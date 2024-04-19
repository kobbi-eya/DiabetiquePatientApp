import { useLocation } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
function HomeMedecin() {
  const { state } = useLocation();
  const idmed_id = state ? state.idmed_id : null;
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1 className="title_medecin">Bienvenue sur votre tableau de bord</h1>
      <div className="sous_container">
        <div className="right">
          <h2>Actions</h2>
          {idmed_id && (
            <button className="register_patient_button" onClick={() => navigate(`/login/registerpatient/${idmed_id}`)}>
              Register a Patient
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default HomeMedecin;

