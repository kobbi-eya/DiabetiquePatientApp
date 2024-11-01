import React, { useState, useEffect } from "react";
import { useParams, Link } from 'react-router-dom';
import '../styles/CarnetMedicale.css';
import infopers from '../images/infopers.png';
import infopers1 from '../images/infopers1.png';
import carnet from '../images/carnet.png';
import api from "../api";
import TabWidget from '../pages/TabWidget';

function CarnetMedicalpat() {
  const { patientId } = useParams();
  const [patientInfo, setPatientInfo] = useState(null);
  const [consultations, setConsultations] = useState([]);
  const [selectedConsultation, setSelectedConsultation] = useState(null);

  useEffect(() => {
    // Appels à l'API pour récupérer les informations du patient et les consultations
    api.get(`/api/patients/${patientId}/`)
      .then((res) => {
        setPatientInfo(res.data);
      })
      .catch((error) => {
        console.error('Error fetching patient information:', error);
      });

    api.get(`/api/consultations/${patientId}/`)
      .then((res) => {
        setConsultations(res.data.consultations);
      })
      .catch((error) => {
        console.error('Error fetching patient consultations:', error);
      });
  }, [patientId]);

  if (!patientInfo) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container">
      <div className="carnet-medical">
        <img src={carnet} alt="carnet" className="carnet" />
        <h1>Carnet Médical</h1>
        <img src={infopers} alt="secret" className="infopers" />
        <TabWidget>
          <div label="Informations personnelles">
            <div className='left'>
              <img src={infopers1} alt="infopers" className="infopers1" />
            </div>
            <div className='right'>
              <p>Nom: {patientInfo.nom}</p>
              <p>Prénom: {patientInfo.prenom}</p>
              <p>Email: {patientInfo.email}</p>
              <p>Date de Naissance: {patientInfo.date_de_naissance}</p>
              <p>Poids: {patientInfo.poids}</p>
              <p>Taille: {patientInfo.taille}</p>
              <p>Allergies: {patientInfo.allergies}</p>
              <p>Type diabète: {patientInfo.type_diabete}</p>
              <p>Groupe Sanguin: {patientInfo.groupe_sanguin}</p>
            </div>
          </div>

          <div label="Consultations">
            <div className="consultations-container">
              {consultations.map((consultation, index) => (
                <button key={consultation.id} onClick={() => setSelectedConsultation(consultation)}>{`Consultation ${index + 1}`}</button>
              ))}
            </div>
            {selectedConsultation && (
              <div className="consultation-details">
                <p>Médecin: {selectedConsultation.medecin}</p>
                <p>Date de consultation: {selectedConsultation.date_consultation}</p>
                <p>Heure de consultation: {selectedConsultation.heure_consultation}</p>
                <p>Ordonnance: {selectedConsultation.ordonnance}</p>
                <p>Description: {selectedConsultation.description}</p>
                <p>Bilan: {selectedConsultation.bilan}</p>
                <p>Bilan PDF: {selectedConsultation.bilan_pdf ? <a href={`http://localhost:8000${selectedConsultation.bilan_pdf}`} target="_blank" rel="noopener noreferrer">Voir le PDF</a> : "Aucun fichier PDF disponible"}</p>
              </div>
            )}
          </div>
        </TabWidget>
      </div>
      <Link to={`/home_patient/${patientId}/`} className="btn btn-primary">Retourner à l'accueil</Link>
    </div>
  );
}

export default CarnetMedicalpat;
