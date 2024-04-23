import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import '../styles/CarnetMedicale.css';
import infopers from './infopers.png';
import infopers1 from './infopers1.png';
import carnet from './carnet.png';
import consult1 from './consult1.png';
import api from "../api";

function CarnetMedical() {
  const { patientId } = useParams(); // Supposons que vous ayez défini le paramètre de l'URL pour l'ID du patient
  const [patientInfo, setPatientInfo] = useState(null);

  useEffect(() => {
    // Appel à l'API pour récupérer les informations du patient
    api.get(`http://localhost:8000/api/patients/${patientId}/`)
      .then((res) => {
        setPatientInfo(res.data);
      })
      .catch((error) => {
        console.error('Error fetching patient information:', error);
      });

     /* api.get(`http://localhost:8000/api/patients/${patientId}/consultations`)
      .then((res) => {
        setConsultations(res.data);
      })
      .catch((error) => {
        console.error('Error fetching patient consultations:', error);
      });*/
  }, [patientId]); // Assurez-vous de mettre à jour la requête lorsque le patientId change
  
  if (!patientInfo) {
    return <div>Loading...</div>; // Afficher un message de chargement tant que les données du patient ne sont pas chargées
  }

  return (
    <div>
      <h1>Informations du Patient</h1>
      <p>Nom: {patientInfo.nom}</p>
      <p>Prénom: {patientInfo.prenom}</p>
      <p>Date de Naissance: {patientInfo.date_de_naissance}</p>
      {/* Afficher d'autres détails du patient ici */}
    </div>
  );
}

export default CarnetMedical;
