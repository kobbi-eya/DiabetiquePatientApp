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
    getRendezVous();
  }, [idmedId]);

  const getRendezVous = () => {
    const processedPatientIds = new Set(); 
    api
      .get(`http://localhost:8000/api/medecin/rendez-vous/${idmedId}/`)
      .then((res) => res.data)
      .then((data) => {
        // Transformez les données des rendez-vous ici
  
        const events = data.rendez_vous.map((rendezVous) => {
          // Récupérer les informations du patient associé à ce rendez-vous
          api
            .get(`http://localhost:8000/api/patients/${rendezVous.idpat}/`)
            .then((res) => res.data)
            .then((patientData) => {
              const title = `${patientData.nom} ${patientData.prenom} (${patientData.email})`;
              // Créer l'événement avec les données récupérées
              const event = {
                start: new Date(rendezVous.date_consultation + ' ' + rendezVous.heure_consultation),
                end: new Date(rendezVous.date_consultation + ' ' + rendezVous.heure_consultation),
                title: title,
                location: rendezVous.location,
              };
              // Ajouter l'événement à la liste des événements
              setRendezVousData((prevEvents) => [...prevEvents, event]);
            })
            .catch((error) => {
              console.error('Error fetching patient details:', error);
            });
        });

      })
      .catch((error) => {
        console.error('Error fetching rendez-vous:', error);
      });
  };

  return (
    <div className="container">
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
/*import { useLocation } from 'react-router-dom';
import React, { useEffect, useState } from "react";
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import api from "../api";
import { useNavigate } from "react-router-dom";
import axios from 'axios'; // Importez axios


const localizer = momentLocalizer(moment);

function HomeMedecin() {
  const { state } = useLocation();
  const idmedId = state ? state.idmed_id : null;
  const navigate = useNavigate();
  const [rendezVousData, setRendezVousData] = useState([]);

  useEffect(() => {
    getRendezVous();
  }, [idmedId]);

  const getRendezVous = () => {
    axios
      .get(`http://localhost:8000/api/medecin//rendez-vous/${idmedId}`)
      .then((res) => res.data)
      .then((data) => {
        setRendezVousData(data);
      })
      .catch((error) => {
        console.error('Error fetching rendez-vous:', error);
      });
  };

  return (
    <div className="container">
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
            </div>
          )}
        </div>
      </div>

      <div style={{ height: 500 }}>
        <Calendar
          localizer={localizer}
          events={rendezVousData.rendez_vous}
          startAccessor="start"
          endAccessor="end"
          style={{ margin: '50px' }}
        />
      </div>
    </div>
  );
}

export default HomeMedecin;*/
