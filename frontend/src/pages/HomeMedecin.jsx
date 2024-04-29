import React, { useEffect, useState } from "react";
import axios from 'axios'; // Importez axios
import { useLocation } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import Calendrier from "../components/Calendrier";
import api from "../api";

function HomeMedecin() {
  const { state } = useLocation();
  const idmedId = state ? state.idmed_id : null;
  const navigate = useNavigate();
  const [rendezVousData, setRendezVousData] = useState([]);
  useEffect(() => {
    if (idmedId) {
      getRendezVous();
    }
  }, [idmedId]);

  const getRendezVous = () => {
    api
      .get(`http://localhost:8000/api/medecin/rendez-vous/${idmedId}/`)
      .then((res) => res.data)
      .then((data) => {
        // Récupérer toutes les promesses de requêtes pour chaque rendez-vous
        const promises = data.rendez_vous.map((rendezVous) => {
          return api.get(`http://localhost:8000/api/patients/${rendezVous.idpat}/`).then((res) => res.data);
        });
  
        // Attendre que toutes les requêtes soient terminées
        Promise.all(promises)
          .then((patientDataArray) => {
            // Créer les événements avec les données récupérées
            const events = data.rendez_vous.map((rendezVous, index) => {
              const patientData = patientDataArray[index];
              const title = `${patientData.nom} ${patientData.prenom} (${patientData.email})`;
              return {
                id: rendezVous.id,
                start: new Date(rendezVous.date_consultation + ' ' + rendezVous.heure_consultation),
                end: new Date(rendezVous.date_consultation + ' ' + rendezVous.heure_consultation),
                title: title,
                location: rendezVous.location,
              };
            });
            // Mettre à jour l'état avec les événements
            setRendezVousData(events);
          })
          .catch((error) => {
            console.error('Error fetching patient details:', error);
          });
      })
      .catch((error) => {
        console.error('Error fetching rendez-vous:', error);
      });
  };
  

  return (
    <div className="container">
      <nav>
        <ul>
          <li>Accueil</li>
          <li>Patients</li>
          <li>Consultations</li>
          <li>Déconnexion</li>
        </ul>
      </nav>
      <h1 className="title_medecin">Bienvenue sur votre tableau de bord</h1>
      <div className="sous_container">
        <div className="right">
          <h2>Actions</h2>
          {idmedId && (
            <div>
              <button className="register_patient_button" onClick={() => navigate(`/login/registerpatient/${idmedId}`)}>
                Register a Patient
              </button>
              <button className="create_rv_button" onClick={() => navigate(`/login/CreateRv/${idmedId}`)}>
                Create a Rendez-vous
              </button>
              <button className="list_patients_button" onClick={() => navigate(`/login/ListePatient/${idmedId}`)}>
                List Patients
              </button>
            </div>
          )}
        </div>
    
      </div>
      {Array.isArray(rendezVousData) && <Calendrier rendezVousData={rendezVousData} />} 
    </div>
  );
}

export default HomeMedecin;
