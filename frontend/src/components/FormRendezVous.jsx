import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import "../styles/CreateRv.css";
import createrv from "./createrv.png";
import api from '../api';
import { useNavigate,useParams } from 'react-router-dom';


// Définition de la fonction fetchPatientIdByEmail
/*const fetchPatientIdByEmail = async (email) => {
    try {
        const response = await api.get(`/api/user/getPatientByEmail/${email}`);
        return response.data.id;
    } catch (error) {
        console.error('Erreur lors de la récupération de l\'ID du patient :', error);
        return null;
    }
};*/

const FormRv = () => {
    const { medecinId } = useParams(); 
    const [rendezVous, setRendezVous] = useState({
        email: '',
        dateConsultation: new Date(),
        heureConsultation: '',
        notes: '',
        idpat:0
    });
    
    const navigate = useNavigate();
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setRendezVous({ ...rendezVous, [name]: value });
    };

    const handleDateChange = (date) => {
        setRendezVous({ ...rendezVous, dateConsultation: date });
    };

    const handleHeureChange = (heure) => {
        setRendezVous({ ...rendezVous, heureConsultation: heure });
    };

   
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const dateFormatted = `${rendezVous.dateConsultation.getFullYear()}-${(rendezVous.dateConsultation.getMonth() + 1).toString().padStart(2, '0')}-${rendezVous.dateConsultation.getDate().toString().padStart(2, '0')}`;
            console.log("Données du formulaire :", rendezVous);
            const response = await api.post(`/api/user/createRv/${medecinId}`, {
                email: rendezVous.email,
                dateConsultation: dateFormatted,
                heureConsultation: rendezVous.heureConsultation,
                notes: rendezVous.notes,
                idpat: rendezVous.idpat,
                idmed: medecinId ? medecinId : 0
            });
            console.log('Réponse de la création du rendez-vous :', response.data);
            // Redirection ou autre traitement après la création du rendez-vous
            if (response.data.success) {
                navigate(`/login/home_medecin/${medecinId}`, { state: { idmed_id: medecinId } });
              } else {
                console.error("L'inscription a échoué.");
              }

        } catch (error) {
            console.error("Erreur lors de la création du rendez-vous :", error);
            if (error.response && error.response.data && error.response.data.error) {
                const errorMessage = error.response.data.error;
                alert(errorMessage); // Afficher l'erreur dans une alerte
            } else if (error.response && error.response.data && error.response.data.type) {
                const errorType = error.response.data.type;
                if (errorType === "creneau_existant") {
                    alert("Ce créneau est déjà pris par un autre patient.");
                } else if (errorType === "patient_invalide") {
                    alert("Vous n'êtes pas autorisé à créer un rendez-vous pour ce patient.");
                } else if (errorType === "intervalle_invalide") {
                    alert("Il doit y avoir un intervalle de 20 minutes minimum entre les rendez-vous.");
                } else {
                    alert("Une erreur inattendue s'est produite. Veuillez réessayer.");
                }
            } else {
                alert("Une erreur est survenue lors de la création du rendez-vous. Veuillez réessayer.");
            }
        }
    };
    
    
    return (
      <div className="container">
        <nav>
         <ul>
          <li onClick={() => navigate(`/login/home_medecin/${medecinId}`)}>Accueil</li>
          <li>Patients</li>
          <li>Consultations</li>
          <li>Déconnexion</li>
          </ul>
        </nav>
            <h1 className="title_rv">Créer un rendez-vous</h1>
            <div className="format">
                <div className="right">
                    <img src={createrv} alt="createrv" className="createrv" />
                </div>
                <div className="left">
                    <div className="sous_container">
                        <form onSubmit={handleSubmit}>
                        <input
                        type="email"
                        name="email"
                        id="email"
                        value={rendezVous.email}
                        placeholder="exemple@gmail.com"
                        onChange={handleInputChange}
                        />
                        <label>
                             Date de consultation:
                             <DatePicker
                                 selected={rendezVous.dateConsultation}
                                 onChange={handleDateChange}
                                 dateFormat="yyyy-MM-dd"
                                 id="dateConsultation"
                                />
                            </label>
                            <label>
                                Heure de consultation:
                                <input
                                    type="time"
                                    value={rendezVous.heureConsultation}
                                    onChange={(e) => handleHeureChange(e.target.value)}
                                    id="heureConsultation"
                                />
                            </label>
                            <label>
                                Description:
                                <textarea
                                    className="notes-textarea"
                                    name="notes"
                                    id="notes"
                                    value={rendezVous.notes}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <button className="confirm-button" type="submit">Confirmer</button>
                            <button className="cancel-button">Annuler</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FormRv;