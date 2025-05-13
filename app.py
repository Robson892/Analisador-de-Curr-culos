import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from extractor import (
    extract_email, extract_phone, extract_linkedin, extract_name,
    extract_skills, extract_languages, extract_experience_years
)
# from sentence_transformers import SentenceTransformer, util  # Descomente se for usar

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def main():
    st.set_page_config(page_title="Analisador de Currículos", layout="wide")
    st.title("📄 Analisador de Currículos com NLP")
    st.markdown("Faça upload de currículos em PDF para analisá-los automaticamente.")

    vaga_input = st.text_input("📋 Insira as habilidades da vaga (separadas por vírgula):", "Python, SQL, Power BI, Git")
    vaga_skills = [s.strip().lower() for s in vaga_input.split(",") if s.strip()]

    uploaded_files = st.file_uploader("📂 Envie um ou mais currículos em PDF", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        candidatos = []
        progress = st.progress(0, text="Analisando currículos...")

        for idx, uploaded_file in enumerate(uploaded_files):
            text = extract_text_from_pdf(uploaded_file)

            nome = extract_name(text)
            email = extract_email(text)
            telefone = extract_phone(text)
            linkedin = extract_linkedin(text)
            skills = extract_skills(text)
            idiomas = extract_languages(text)
            experiencia = extract_experience_years(text)

            habilidades_curriculo = [s.lower() for s in skills]
            encontrados = [s for s in vaga_skills if s in habilidades_curriculo]
            score = int((len(encontrados) / len(vaga_skills)) * 100) if vaga_skills else 0

            candidatos.append({
                "Nome": nome,
                "E-mail": email or "Não encontrado",
                "Telefone": telefone or "Não encontrado",
                "LinkedIn": linkedin or "Não encontrado",
                "Skills encontradas": ", ".join(encontrados),
                "Idiomas": ", ".join(idiomas) if idiomas else "Não identificado",
                "Experiência (anos)": experiencia,
                "Score (%)": score
            })

            progress.progress((idx + 1) / len(uploaded_files), text=f"Analisando: {nome or 'Currículo'}")

        st.success(f"{len(uploaded_files)} currículo(s) analisado(s) com sucesso!")

        # Exibir tabela
        df = pd.DataFrame(candidatos).sort_values(by="Score (%)", ascending=False)
        st.subheader("📊 Ranking de Aderência")
        st.dataframe(df, use_container_width=True)

        # Exportação CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Ranking (CSV)", csv, "ranking.csv", "text/csv")

        # Exportação Excel
        import io

        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        st.download_button(
            "📥 Baixar Ranking (Excel)",
            data=excel_buffer.getvalue(),
            file_name="ranking.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


        # Comparação semântica (opcional - requer instalação)
        # st.subheader("🧠 Comparação Semântica (Beta)")
        # model = SentenceTransformer("all-MiniLM-L6-v2")
        # vaga_embed = model.encode(vaga_input, convert_to_tensor=True)
        # for c in candidatos:
        #     skills_embed = model.encode(c["Skills encontradas"].split(", "), convert_to_tensor=True)
        #     similarity = util.cos_sim(skills_embed, vaga_embed).mean().item()
        #     st.write(f"{c['Nome']}: Similaridade Semântica: {similarity:.2f}")

if __name__ == "__main__":
    main()
