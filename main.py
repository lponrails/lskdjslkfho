import streamlit as st

st.set_page_config(
    page_title="Jornada Marandu | LP on Rails", page_icon="👁️", layout="wide"
)

st.write("# Jornada Marandu | LP on Rails")
st.sidebar.success("Selecione uma das páginas acima")


st.markdown(
    """
    <style>
        .container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .profile-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin-right: 15px;
            background-color: #ddd;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 30px;
            color: #aaa;
        }
        .info {
            font-size: 14px;
        }
        .info strong {
            font-size: 16px;
        }
        .divider {
            border-top: 2px solid #000;
            margin: 10px 0;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown("## **Desafio Proposto:**")
st.info(
    "🚂🛤️ Reconhecimento por Imagem para Identificação de Defeitos nos Trilhos da Estrada de Ferro Carajás."
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("### **Membros:**")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# Function to create a profile section
def profile_section(name, role):
    st.markdown(
        f"""
        <div class="container">
            <div class="profile-img">👤</div>
            <div class="info">
                <strong>{name}</strong><br>
                {role}
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )


# Members
profile_section("ANTONIO F. L. JACOB JR.", "Professor Orientador")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

profile_section(
    "ADRIELSON F. JUSTINO",
    "Cientista da Computação<br>Mestrando - Eng. da Computação e Sistemas",
)
profile_section(
    "GUSTAVO S. SILVA",
    "Engenheiro da Computação<br>Mestrando - Eng. da Computação e Sistemas",
)
profile_section("HÉVILA S. DE FREITAS", "Graduanda em Engenharia da Computação")
profile_section("PEDRO B. LEAL", "Graduando em Engenharia de Produção")
profile_section("RENAN VICTOR D. COSTA", "Graduando em Engenharia da Computação")
profile_section("JONAS C. DE S. NETO", "Graduando em Engenharia da Computação")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("### Product Owner (PO):")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

profile_section("JOCIKLEY MACHADO", "Product Owner")
