import streamlit as st
import pandas as pd
import joblib
import sys
import os
import shap
import matplotlib.pyplot as plt
from lime.lime_tabular import LimeTabularExplainer
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

SRC_PATH = os.path.join(PROJECT_ROOT, "src")
MODELS_PATH = os.path.join(PROJECT_ROOT, "models")

# Streamlit requires page configuration before any UI output.
st.set_page_config(
    page_title="Explainable Phishing URL Detector",
    page_icon="🔎",
    layout="wide"
)

# --------------------------------------------------
# Load external CSS
# --------------------------------------------------

def load_css():
    css_path = os.path.join(
        os.path.dirname(__file__),
        "style.css"
    )

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from feature_extraction import extract_url_features
from url_validation import validate_url_input
from lime_formatting import format_lime_condition


# --------------------------------------------------
# Load trained model and feature list
# --------------------------------------------------

@st.cache_resource
def load_model():
    model = joblib.load(
        
        os.path.join(MODELS_PATH, "phishing_detector_final.pkl")
    )
    print("MODEL CLASSES:", model.classes_)

    feature_columns = joblib.load(
        os.path.join(MODELS_PATH, "feature_columns_final.pkl")
    )

    return model, feature_columns


model, feature_columns = load_model()
@st.cache_resource
def load_shap_explainer():
    background_data = pd.read_csv(
        os.path.join(
            PROJECT_ROOT,
            "data",
            "processed",
            "phishing_url_features_v2.csv"
        )
    )

    X_background = background_data[feature_columns]

    # Use a small representative sample to keep the app responsive
    X_background = shap.sample(
        X_background,
        100,
        random_state=42
    )

    explainer = shap.Explainer(
        model,
        X_background
    )

    return explainer


shap_explainer = load_shap_explainer()
@st.cache_resource
def load_lime_explainer():

    data = pd.read_csv(
        os.path.join(
            PROJECT_ROOT,
            "data",
            "processed",
            "phishing_url_features_v2.csv"
        )
    )

    X_lime = data[feature_columns]

    explainer = LimeTabularExplainer(
        training_data=X_lime.values,
        feature_names=feature_columns,
        class_names=["Phishing", "Legitimate"],
        mode="classification",
        random_state=42
    )

    return explainer


lime_explainer = load_lime_explainer()


# --------------------------------------------------
# Page configuration
# --------------------------------------------------


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.markdown("""
<div class="main-header">
    <h1>🛡️ PhishGuard XAI</h1>
    <p>Explainable Machine Learning for Phishing URL Detection</p>
    <div class="badge-container">
        <span class="badge">Machine Learning</span>
        <span class="badge">SHAP</span>
        <span class="badge">LIME</span>
        <span class="badge">Explainable AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-card">
    <div class="section-title">🔍 Analyse a URL</div>
    <div class="section-description">
        Enter a web address below to assess whether its URL characteristics are associated with phishing or legitimate websites.
    </div>
</div>
""", unsafe_allow_html=True)

# st.title("Explainable Phishing URL Detector")

# st.write(
#     "Enter a URL below to analyse whether it is likely "
#     "to be phishing or legitimate."
# )


# --------------------------------------------------
# URL input
# --------------------------------------------------
url = st.text_input(
    "Enter URL",
    placeholder="https://www.example.com"
)


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("Analyse URL"):

    validation_status, validation_text = validate_url_input(url)

    if validation_status == "warning":
        st.warning(validation_text)
    elif validation_status == "error":
        st.error(validation_text)
    else:
        try:
            # Only validated URLs reach feature extraction / prediction.
            # Extract URL features
            features = extract_url_features(url)
            print("\nURL:", url)
            print("EXTRACTED FEATURES:")
            for name, value in features.items():
                print(f"{name}: {value}")

            features_df = pd.DataFrame(
                [features],
                columns=feature_columns
            )

            # Make prediction
            prediction = model.predict(features_df)[0]

            probabilities = model.predict_proba(
                features_df
            )[0]

            phishing_index = list(model.classes_).index(0)
            legitimate_index = list(model.classes_).index(1)

            phishing_probability = (
                probabilities[phishing_index] * 100
            )

            legitimate_probability = (
                probabilities[legitimate_index] * 100
            )

            # ------------------------------------------
            # Display prediction
            # ------------------------------------------

            st.markdown("## Analysis Result")
            st.markdown(f"**Analysed URL:** `{url}`")

            if prediction == 0:
                st.error("⚠️ Prediction: PHISHING")
            else:
                st.success("✅ Prediction: LEGITIMATE")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Phishing Probability",
                    f"{phishing_probability:.2f}%"
                )

            with col2:
                st.metric(
                    "Legitimate Probability",
                    f"{legitimate_probability:.2f}%"
                )

            # ------------------------------------------
            # SHAP explanation
            # ------------------------------------------
            st.caption(
                "The SHAP chart shows how individual URL "
                "features influenced this prediction."
            )
            

            st.divider()

            st.subheader(
                "Why did the model make this prediction?"
            )

            st.write(
                "The explanation below shows which URL "
                "characteristics had the greatest influence "
                "on the model's prediction."
            )
            
            # Explain the SHAP colour direction correctly.
# For this binary classifier, SHAP values describe movement
# toward or away from class 1 (Legitimate).

            if prediction == 0:
                st.info(
                    "How to read this explanation: blue features pushed the model "
                    "away from legitimate and therefore towards the phishing prediction, "
                    "while red features pushed the model towards legitimate. "
                    "Longer bars had a greater influence on the prediction."
                )
            else:
                st.info(
                    "How to read this explanation: red features pushed the model "
                    "towards the legitimate prediction, while blue features pushed "
                    "the model away from legitimate and towards phishing. "
                    "Longer bars had a greater influence on the prediction."
                )

            shap_values = shap_explainer(features_df)

            # Friendly feature names for the SHAP chart
            shap_friendly_names = {
                "url_length": "URL length",
                "domain_length": "Domain length",
                "path_length": "Path length",
                "query_length": "Query length",
                "tld_length": "Top-level domain length",
                "subdomain_count": "Number of subdomains",
                "is_domain_ip": "Domain is an IP address",
                "digit_count": "Number of digits",
                "letter_count": "Number of letters",
                "dot_count": "Number of dots",
                "hyphen_count": "Number of hyphens",
                "underscore_count": "Number of underscores",
                "slash_count": "Number of slashes",
                "question_mark_count": "Number of question marks",
                "equals_count": "Number of equals signs",
                "ampersand_count": "Number of ampersands",
                "at_symbol_count": "Number of @ symbols",
                "percent_count": "Number of % symbols",
                "special_char_count": "Number of special characters",
                "is_https": "HTTPS enabled"
            }

            # Make a copy so the original SHAP explanation is unchanged
            shap_display = shap_values[0]

            shap_display.feature_names = [
                shap_friendly_names.get(name, name)
                for name in features_df.columns
            ]

            shap.plots.waterfall(
                shap_display,
                max_display=10,
                show=False
            )

            st.pyplot(
                plt.gcf(),
                clear_figure=True
            )

            st.caption(
                "The SHAP chart shows how individual URL "
                "features influenced this prediction."
            )
            
            # ------------------------------------------
            # LIME explanation
            # ------------------------------------------

            st.divider()

            st.subheader("LIME Explanation")

            st.write(
                "LIME provides a second local explanation of the prediction "
                "by showing which URL characteristics influenced the result."
            )
            
            if prediction == 0:
                st.info(
                    "How to read this explanation: positive contributions support "
                    "the phishing prediction, while negative contributions push "
                    "the prediction towards legitimate."
                )
            else:
                st.info(
                    "How to read this explanation: positive contributions support "
                    "the legitimate prediction, while negative contributions push "
                    "the prediction towards phishing."
                )

            lime_explanation = lime_explainer.explain_instance(
                features_df.iloc[0].values,
                model.predict_proba,
                num_features=10,
                labels=[prediction]
            )

            lime_results = pd.DataFrame(
                lime_explanation.as_list(label=prediction),
                columns=["Feature condition", "Contribution"]
            )
            
            # Preserve LIME's <=, > and bounded inequalities exactly:
            # the former formatter wrongly called every threshold "or fewer".
            lime_results["Feature condition"] = lime_results[
                "Feature condition"
            ].apply(format_lime_condition)

            st.dataframe(
                lime_results,
                use_container_width=True
            )

            # Get LIME contributions for the predicted class
            lime_chart_data = lime_explanation.as_list(label=prediction)

            # Display matching readable intervals in the plot and table.
            feature_names = [
                format_lime_condition(item[0]) for item in lime_chart_data
            ]
            contributions = [item[1] for item in lime_chart_data]

            # Sort by contribution
            order = np.argsort(np.abs(contributions))

            feature_names = [feature_names[i] for i in order]
            contributions = [contributions[i] for i in order]

            # Professional chart colours
            colors = [
                "#2563eb" if value > 0 else "#ef4444"
                for value in contributions
            ]

            # Create chart
            fig, ax = plt.subplots(figsize=(11, 6.5))

            fig.patch.set_facecolor("#ffffff")
            ax.set_facecolor("#ffffff")

            bars = ax.barh(
                feature_names,
                contributions,
                color=colors,
                height=0.58
            )

            # Zero reference line
            ax.axvline(
                0,
                color="#94a3b8",
                linewidth=1
            )

            # Remove unnecessary borders
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Subtle horizontal grid
            ax.grid(
                axis="x",
                linestyle="--",
                alpha=0.15
            )

            ax.set_axisbelow(True)

            # Titles
            class_name = (
                "Phishing" if prediction == 0
                else "Legitimate"
            )

            ax.set_title(
                f"Factors Influencing the {class_name} Prediction",
                fontsize=15,
                fontweight="bold",
                color="#0f172a",
                pad=20
            )

            ax.set_xlabel(
                "Contribution to the prediction",
                fontsize=11,
                color="#475569"
            )

            ax.tick_params(
                axis="both",
                labelsize=10,
                colors="#334155",
                length=0
            )

            # Improve spacing
            plt.tight_layout()

            # Display in Streamlit
            st.pyplot(fig, width="stretch")

            # plt.close(fig)
            # st.pyplot(
            #     lime_fig,
            #     clear_figure=True
            # )

            st.caption(
                "The LIME chart shows the features that locally influenced "
                "the model's prediction for this URL."
            )
            # --------------------------------------------------
            # Plain-English explanation
            # --------------------------------------------------

            st.divider()
            st.subheader("What does this mean?")

            if prediction == 0:
                st.warning(
                    "The model detected URL characteristics that are commonly "
                    "associated with phishing links. Review the explanation below "
                    "before deciding whether to trust the website."
                )
            else:
                st.success(
                    "The URL characteristics examined by the model are more "
                    "consistent with legitimate URLs in the training data."
                )

            st.write("### Key URL characteristics")

            feature_descriptions = {
                "url_length": "Length of the URL",
                "domain_length": "Length of the domain name",
                "is_domain_ip": "Whether an IP address is used instead of a domain name",
                "subdomain_count": "Number of subdomains",
                "digit_count": "Number of digits in the URL",
                "letter_count": "Number of letters in the URL",
                "special_char_count": "Number of special characters",
                "slash_count": "Number of slashes in the URL",
                "question_mark_count": "Number of question marks",
                "equals_count": "Number of equals signs",
                "at_symbol_count": "Number of @ symbols",
                "hyphen_count": "Number of hyphens",
                "underscore_count": "Number of underscores",
                "percent_count": "Number of percentage symbols",
                "tld_length": "Length of the top-level domain",
                "is_https": "Whether the URL uses HTTPS"
            }

            important_features = []

            for feature in feature_columns:
                if feature in feature_descriptions:
                    value = features_df.iloc[0][feature]

                    important_features.append(
                        {
                            "Characteristic": feature_descriptions[feature],
                            "Observed value": value
                        }
                    )

            explanation_df = pd.DataFrame(important_features)

            st.dataframe(
                explanation_df,
                width="stretch",
                hide_index=True
            )

            st.caption(
                "These characteristics are analysed by the machine-learning model. "
                "They should not be interpreted individually as proof that a website "
                "is safe or malicious."
            )
            

        except Exception as e:

            st.error("The URL could not be analysed.")

            st.write(
                "Technical details:",
                str(e)
            )
            
            # =========================================================
# APPLICATION FOOTER
# =========================================================

# =========================================================
# PROFESSIONAL APPLICATION FOOTER
# =========================================================

st.markdown("---")

footer_html = (
    '<div style="background:linear-gradient(135deg,#0f172a,#1e3a5f);'
    'padding:35px 25px;border-radius:14px;text-align:center;'
    'margin-top:30px;box-shadow:0 8px 24px rgba(15,23,42,0.15);">'
    '<h3 style="color:white;margin-bottom:12px;">'
    'Explainable Phishing URL Detection</h3>'
    '<p style="color:#cbd5e1;">'
    'MSc Information Technology | UWE Bristol</p>'
    '<p style="color:#93c5fd;">'
    'Machine Learning • SHAP • LIME</p>'
    '<p style="color:#cbd5e1;font-size:13px;line-height:1.7;'
    'max-width:650px;margin:20px auto;">'
    'Research prototype. Predictions are advisory and should not '
    'be treated as definitive evidence that a website is safe or malicious.'
    '</p>'
    '<div style="border-top:1px solid #334155;padding-top:18px;'
    'margin-top:20px;color:#94a3b8;font-size:12px;">'
    '© 2027 | MSc Research Project'
    '</div>'
    '</div>'
)

st.markdown(footer_html, unsafe_allow_html=True)