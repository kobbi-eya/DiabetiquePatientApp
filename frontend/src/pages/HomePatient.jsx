import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import api from "../api";

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

  return (
    <div>
      <h1>Home Patient</h1>
      <button className="create_rv_button" onClick={handleConsultMedicalRecord}>
        Consulter le carnet médical
      </button>
    </div>
  );
}

export default HomePatient;
