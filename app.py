import io
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ОГООТ ХХК - Дотоод Эрсдэлийн Бүртгэл", layout="wide"
)

st.title("🛡️ ОГООТ ХХК - Дотоод Эрсдэлийн Бүртгэл (Risk Register)")
st.write(
    "Энэхүү систем нь салбар, хэлтэс тус бүрээр эрсдэлийг сонгож бүртгэх,"
    " үнэлэх болон хэм хэмжээг хянах зориулалттай."
)

DATA_FILE = "ogoot_risk_register_data.csv"


# Өгөгдөл ачаалах болон хадгалах функцууд
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE, encoding="utf-8-sig")
        except Exception:
            pass
    return pd.DataFrame(
        columns=[
            "ID",
            "Салбар / Хэлтэс",
            "Эрсдэлийн тодорхойлолт",
            "Хүлээн зөвшөөрөх хэм хэмжээ",
            "Магадлал (1-5)",
            "Нөлөөлөл (1-5)",
            "Эрсдэлийн түвшин",
            "Хариуцах эзэн",
            "Төлөв",
        ]
    )


# Өгөгдлийг session_state дээр хадгалж тогтвортой болгох
if "df" not in st.session_state:
    st.session_state.df = load_data()

# --- ХУРААНГУЙ МЭДЭЭЛЭЛ (DASHBOARD METRICS) ---
st.markdown("### 📊 Ерөнхий үзүүлэлтүүд")
col1, col2, col3 = st.columns(3)

current_df = st.session_state.df
total_risks = len(current_df)
open_risks = (
    len(current_df[current_df["Төлөв"] == "Нээлттэй"])
    if not current_df.empty and "Төлөв" in current_df.columns
    else 0
)
high_risks = (
    len(current_df[current_df["Эрсдэлийн түвшин"] >= 15])
    if not current_df.empty and "Эрсдэлийн түвшин" in current_df.columns
    else 0
)

col1.metric("Нийт бүртгэгдсэн эрсдэл", total_risks)
col2.metric("Нээлттэй төлөвтэй", open_risks)
col3.metric("Өндөр эрсдэлтэй (Түвшин >= 15)", high_risks)

st.markdown("---")

# Салбар тус бүрийн эрсдэл болон хүлээн зөвшөөрөх хэм хэмжээ
department_risks = {
    "Тээврийн менежер": [
        {
            "risk": (
                "Тээврийн хэрэгслийн гэнэтийн эвдрэл, ашиглалтын буруу горимоос"
                " үүдэн тээвэрлэлт саатах"
            ),
            "threshold": "Зөвшөөрөгдөх түвшин < 10",
        },
        {
            "risk": "Жолоочийн аюулгүй ажиллагааны дүрэм зөрчих эрсдэл",
            "threshold": "Зөвшөөрөгдөх түвшин < 6",
        },
        {
            "risk": "Зам тээврийн ослын улмаас бараа бүтээгдэхүүн гэмтэх",
            "threshold": "Зөвшөөрөгдөх түвшин < 5",
        },
        {
            "risk": (
                "Шатахуун зарцуулалт болон логистикийн төлөвлөлт алдагдах"
            ),
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
        {
            "risk": "Бусад (Гараар бичих)",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
    ],
    "Санхүү": [
        {
            "risk": "Төсөв хэтрэх эсвэл санхүүгийн урсгал доголдох",
            "threshold": "Зөвшөөрөгдөх түвшин < 10",
        },
        {
            "risk": "Тайлан тооцоо хоцрох, алдаа гарах",
            "threshold": "Зөвшөөрөгдөх түвшин < 6",
        },
        {
            "risk": "Авлага барагдуулалт удаашрах",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
        {
            "risk": "Бусад (Гараар бичих)",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
    ],
    "Хүний нөөц": [
        {
            "risk": "Ажилтнуудын тогтворгүй байдал, урсгал ихсэх",
            "threshold": "Зөвшөөрөгдөх түвшин < 9",
        },
        {
            "risk": "Хөдөлмөр хамгаалал, аюулгүй байдлын зөрчил гарах",
            "threshold": "Зөвшөөрөгдөх түвшин < 5",
        },
        {
            "risk": "Сургалт дутуу эсвэл мэдлэг дутагдах",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
        {
            "risk": "Бусад (Гараар бичих)",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
    ],
    "Үйл ажиллагаа": [
        {
            "risk": "Үндсэн үйл ажиллагааны тасалдал үүсэх",
            "threshold": "Зөвшөөрөгдөх түвшин < 9",
        },
        {
            "risk": "Гэрээ хэлцлийн үүргээ хугацаандаа биелүүлэхгүй байх",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
        {
            "risk": "Бусад (Гараар бичих)",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
    ],
    "Технологи / IT": [
        {
            "risk": "Системийн болон сервер доголдох, дата устах",
            "threshold": "Зөвшөөрөгдөх түвшин < 6",
        },
        {
            "risk": "Кибер аюулгүй байдлын эрсдэл",
            "threshold": "Зөвшөөрөгдөх түвшин < 5",
        },
        {
            "risk": "Бусад (Гараар бичих)",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
    ],
    "Хууль эрх зүй": [
        {
            "risk": "Хууль тогтоомжийн өөрчлөлтөд цаг алдах",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
        {
            "risk": "Байгууллагын бичиг баримтын зөрчил үүсэх",
            "threshold": "Зөвшөөрөгдөх түвшин < 6",
        },
        {
            "risk": "Бусад (Гараар бичих)",
            "threshold": "Зөвшөөрөгдөх түвшин < 8",
        },
    ],
}

# Зүүн талын цэс: Шинэ эрсдэл нэмэх хэсэг
st.sidebar.header("➕ Шинэ эрсдэл бүртгэх")

department = st.sidebar.selectbox(
    "Салбар / Хэлтэс", list(department_risks.keys())
)

# Тухайн салбарын эрсдэлийн жагсаалт болон хэм хэмжээг авах
risk_items = department_risks[department]
risk_names = [item["risk"] for item in risk_items]

selected_risk_option = st.sidebar.selectbox(
    "Эрсдэлийн тодорхойлолт сонгох", risk_names
)

# Сонгосон эрсдэлд харгалзах хүлээн зөвшөөрөх хэм хэмжээг автоматаар шүүж гаргах
current_threshold = next(
    item["threshold"] for item in risk_items if item["risk"] == selected_risk_option
)
st.sidebar.info(f"📌 **Хүлээн зөвшөөрөх хэм хэмжээ:** {current_threshold}")

custom_desc = st.sidebar.text_area("Хэрэв 'Бусад' бол энд дэлгэрэнгүй бичнэ үү", "")

likelihood = st.sidebar.slider("Магадлал (1: Бага - 5: Өндөр)", 1, 5, 3)
impact = st.sidebar.slider("Нөлөөлөл (1: Бага - 5: Өндөр)", 1, 5, 3)
owner = st.sidebar.text_input("Хариуцах эзэн / Ажилтан")
status = st.sidebar.selectbox("Төлөв", ["Нээлттэй", "Хянагдаж буй", "Хаагдсан"])

submitted = st.sidebar.button("Бүртгэх")

if submitted:
    if selected_risk_option == "Бусад (Гараар бичих)":
        description = custom_desc.strip()
    else:
        description = selected_risk_option

    if not description:
        st.sidebar.error("Эрсдэлийн тодорхойлолтыг хоосон орхиж болохгүй!")
    else:
        risk_score = likelihood * impact
        new_id = (
            len(st.session_state.df) + 1
            if not st.session_state.df.empty
            else 1
        )

        new_row = {
            "ID": new_id,
            "Салбар / Хэлтэс": department,
            "Эрсдэлийн тодорхойлолт": description,
            "Хүлээн зөвшөөрөх хэм хэмжээ": current_threshold,
            "Магадлал (1-5)": likelihood,
            "Нөлөөлөл (1-5)": impact,
            "Эрсдэлийн түвшин": risk_score,
            "Хариуцах эзэн": owner,
            "Төлөв": status,
        }

        new_df = pd.DataFrame([new_row])
        st.session_state.df = pd.concat(
            [st.session_state.df, new_df], ignore_index=True
        )

        st.session_state.df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
        st.sidebar.success("Эрсдэл амжилттай бүртгэгдлээ!")
        st.rerun()

# Үндсэн хэсэг: Жагсаалт болон шүүлтүүр
st.subheader("📋 Бүртгэгдсэн эрсдэлүүдийн дэлгэрэнгүй жагсаалт")

if st.session_state.df.empty:
    st.info(
        "Одоогоор бүртгэгдсэн эрсдэл байхгүй байна. Зүүн талын цэснээс шинээр"
        " нэмнэ үү."
    )
else:
    selected_dept = st.selectbox(
        "🔍 Салбар / Хэлтсийн шүүлтүүрээр харах",
        ["Бүгд"] + list(st.session_state.df["Салбар / Хэлтэс"].unique()),
    )

    if selected_dept != "Бүгд":
        filtered_df = st.session_state.df[
            st.session_state.df["Салбар / Хэлтэс"] == selected_dept
        ]
    else:
        filtered_df = st.session_state.df

    st.dataframe(filtered_df, use_container_width=True)


    # Excel (.xlsx) файлаар татах функц
    def to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Risk Register")
        return output.getvalue()


    excel_data = to_excel(filtered_df)
    st.download_button(
        label="📥 Шүүгдсэн датаг Excel (.xlsx) файлаар татах",
        data=excel_data,
        file_name="Ogoot_Risk_Register_Filtered.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )