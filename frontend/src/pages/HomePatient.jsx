import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import api from "../api";
import ChangeDoctorForm from "../components/FormChangementDoctor";
function HomePatient() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const { patientId } = useParams(); // Récupérer l'ID du patient à partir des paramètres d'URL

  useEffect(() => {
    // Utiliser l'ID récupéré pour le patient
    console.log("Patient ID:", patientId);
  }, [patientId]);

  const handleConsultMedicalRecord = () => {
    if (patientId) {
      navigate(`/carnet_medical/${patientId}`);
    }
  };
  const handleRequestChangeDoctor = () => {
    if (patientId) {
      navigate(`/DemandeChangementDoctor/${patientId}`);
    }
  };
  const handleAgenda = () => {
    if (patientId) {
      navigate(`/Agenda/${patientId}`);
    }
  };

  return (
    <div>
      <h1>Home Patient</h1>
      <button className="create_rv_button" onClick={handleConsultMedicalRecord}>
        Consulter le carnet médical
      </button>
      <button className="request_change_doctor_button" onClick={handleRequestChangeDoctor}>
        Demander un changement de médecin
      </button>
      <button className="request_change_doctor_button" onClick={handleAgenda}>
        Agenda
      </button>
      
    </div>
  );
}

export default HomePatient;
