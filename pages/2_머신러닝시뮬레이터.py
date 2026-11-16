"""붓꽃(Iris) 4개 특징을 사용한 SVM 지도학습 분류 실습."""
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from ui import page_header
from auth import require_login

require_login()
page_header("LESSON 03 · INTERACTIVE LAB", "붓꽃 품종 예측 시뮬레이터",
            "꽃받침과 꽃잎의 크기를 입력하면 SVM 모델이 붓꽃의 품종을 예측합니다.")

@st.cache_resource(show_spinner=False)
def train_model():
    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma="scale"))
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return iris, model, X_train, X_test, y_train, y_test, y_pred

iris, model, X_train, X_test, y_train, y_test, y_pred = train_model()
feature_names = list(iris.feature_names)
kr_names = ["꽃받침 길이", "꽃받침 너비", "꽃잎 길이", "꽃잎 너비"]
kr_species = ["세토사 (setosa)", "버시컬러 (versicolor)", "버지니카 (virginica)"]

st.markdown("## 1. 붓꽃 특징값 입력")
st.caption("단위는 cm입니다. 4개 입력 특징을 모두 사용하여 예측하며, 기본값은 실습용 예시입니다.")

with st.form("iris_form"):
    cols = st.columns(2, gap="large")
    defaults = [5.1, 3.5, 1.4, 0.2]
    values = []
    for idx, (label, name) in enumerate(zip(kr_names, feature_names)):
        with cols[idx % 2]:
            values.append(st.number_input(
                f"{label} (cm)", min_value=0.0, max_value=12.0,
                value=defaults[idx], step=0.1, format="%.1f", key=f"feature_{idx}",
                help=f"모델이 사용하는 입력 특징: {name}. 0~12 cm 범위에서 입력할 수 있습니다."
            ))
    submitted = st.form_submit_button("🌸 붓꽃 품종 예측하기", type="primary", width="stretch")

if submitted:
    new_sample = pd.DataFrame([values], columns=feature_names)
    predicted = int(model.predict(new_sample)[0])
    st.success(f"예측된 품종: **{kr_species[predicted]}**")
    out1, out2 = st.columns([1, 1.3], gap="large")
    with out1:
        st.markdown("#### 입력한 특징")
        st.dataframe(pd.DataFrame({"측정 항목": kr_names, "입력값 (cm)": values}), hide_index=True, width="stretch")
    with out2:
        st.markdown("#### 예측 결과 해석")
        st.markdown(f"모델이 입력된 4개의 특징을 종합해 **{kr_species[predicted]}**로 분류했습니다.")
        st.info("SVM의 결정 점수는 확률이 아닙니다. 이 시뮬레이터는 확률이나 확신도를 표시하지 않습니다.")
    ranges = [(float(iris.data[c].min()), float(iris.data[c].max())) for c in feature_names]
    outside = [kr_names[i] for i, val in enumerate(values) if not (ranges[i][0] <= val <= ranges[i][1])]
    if outside:
        st.warning("입력값 중 학습 데이터에서 관측된 범위를 벗어난 특징이 있습니다: " + ", ".join(outside) + ". 예측 신뢰도가 낮을 수 있습니다.")
else:
    st.info("네 가지 특징값을 입력한 다음 **붓꽃 품종 예측하기** 버튼을 누르세요.")

st.markdown("## 2. 머신러닝 모델은 어떻게 학습했을까요?")
st.markdown("""
이 시뮬레이터는 scikit-learn에 포함된 **Iris 데이터(총 150개 표본, 3개 품종)** 를 사용합니다.
전체 표본을 **학습 데이터 120개(80%)** 와 **평가 데이터 30개(20%)** 로 구분합니다.
각 특징을 표준화한 뒤 **SVM(Support Vector Machine, 서포트 벡터 머신)** 의 RBF 커널로 분류 경계를 학습합니다.
평가 데이터는 모델 학습에 사용하지 않습니다.
""")
acc = accuracy_score(y_test, y_pred)
m1, m2, m3 = st.columns(3)
m1.metric("전체 표본", f"{len(iris.data)}개")
m2.metric("평가 표본", f"{len(X_test)}개")
m3.metric("평가 정확도", f"{acc:.1%}")
st.caption("평가 정확도는 고정된 데이터 분할(random_state=42)에 대한 값입니다. 모델이 모든 꽃을 동일한 정확도로 구분한다는 뜻은 아닙니다.")

with st.expander("품종별 분류 결과(혼동행렬) 확인"):
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2])
    matrix = pd.DataFrame(cm, index=iris.target_names, columns=iris.target_names)
    matrix.index.name = "실제 품종 ↓ / 예측 품종 →"
    st.dataframe(matrix, width="stretch")
    st.caption("대각선 값은 올바르게 분류한 개수이고, 대각선 밖 값은 잘못 분류한 개수입니다.")

st.markdown("## 3. 데이터로 패턴 확인하기")
plot_df = iris.frame.copy()
plot_df["품종"] = plot_df["target"].map(dict(enumerate(iris.target_names)))
# Streamlit 기본 산점도 사용: Plotly 추가 설치가 필요하지 않습니다.
st.scatter_chart(
    plot_df,
    x=feature_names[2],
    y=feature_names[3],
    color="품종",
    height=440,
    width="stretch",
)
st.caption("산점도는 꽃잎의 두 특징만 시각화한 것입니다. 실제 SVM 예측에는 네 특징을 모두 사용합니다.")

with st.expander("원본 붓꽃 데이터 일부 보기"):
    preview = iris.frame.copy()
    preview["품종"] = preview["target"].map(dict(enumerate(iris.target_names)))
    st.dataframe(preview.drop(columns=["target"]).head(20), width="stretch", hide_index=True)

st.markdown("## 4. 탐구 과제")
st.markdown("""
1. 꽃잎 길이와 꽃잎 너비를 작게 입력했을 때 어떤 품종이 나오는지 관찰해 보세요.
2. **꽃받침 길이**만 바꿔서 결과가 달라지는 구간이 있는지 확인해 보세요.
3. 서로 다른 품종 사이의 특징값을 입력했을 때 결과가 바뀌는 이유를 설명해 보세요.
4. 입력값이 학습 데이터 범위를 벗어나면 모델을 얼마나 믿을 수 있을지 토의해 보세요.
""")
st.caption("데이터 출처: Fisher의 붓꽃 데이터셋(scikit-learn 내장). 이 교육용 예제는 실제 식물 감정 도구가 아닙니다.")
