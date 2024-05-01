import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import '../styles/CarnetMedicale.css';
import infopers from '../images/infopers.png';
import infopers1 from '../images/infopers1.png';
import carnet from '../images/carnet.png';
import consult1 from '../images/consult1.png';
import api from "../api";
import TabWidget from '../pages/TabWidget'; // Assurez-vous que le chemin d'importation est correct

function CarnetMedical() {
  const { patientId } = useParams();
  const [patientInfo, setPatientInfo] = useState(null);
  const [consultations, setConsultations] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editedPatientInfo, setEditedPatientInfo] = useState({
    poids: '',
    taille: '',
    allergies: ''
  });

  useEffect(() => {
    // Appels à l'API pour récupérer les informations du patient
    api.get(`http://localhost:8000/api/patients/${patientId}/`)
      .then((res) => {
        setPatientInfo(res.data);
        setEditedPatientInfo(res.data); // Initialise les informations éditées avec les données actuelles
      })
      .catch((error) => {
        console.error('Error fetching patient information:', error);
      });

  }, [patientId]);

  const handleshowConsultations = () => {
    api.get(`http://localhost:8000/api/consultations/${patientId}/`)
      .then((res) => {
        setConsultations(res.data.consultations);
      })
      .catch((error) => {
        console.error('Error fetching patient consultations:', error);
      });
    
  };
  
  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditedPatientInfo(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = () => {
    setPatientInfo(editedPatientInfo);
    // Envoyer les informations mises à jour à l'API
    api.put(`http://localhost:8000/api/patients/update/${patientId}/`, editedPatientInfo)
      .then((res) => {
        //setPatientInfo(res.data);
        setIsEditing(false); // Désactive le mode édition après la mise à jour
      })
      .catch((error) => {
        console.error('Error updating patient information:', error);
      });
  };
  useEffect(() => {
    handleshowConsultations();
  }, []);
  

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
              {isEditing ? (
                <>
                  <label>Poids:</label>
                  <input type="text" name="poids" value={editedPatientInfo.poids} onChange={handleInputChange} />
                  <label>Taille:</label>
                  <input type="text" name="taille" value={editedPatientInfo.taille} onChange={handleInputChange} />
                  <label>Allergies:</label>
                  <input type="text" name="allergies" value={editedPatientInfo.allergies} onChange={handleInputChange} />
                  <button onClick={handleSubmit}>Enregistrer</button>
                </>
              ) : (
                <>
                  <p>Nom: {patientInfo.nom}</p>
                  <p>Prénom: {patientInfo.prenom}</p>
                  <p>email: {patientInfo.email}</p>
                  <p>Date de Naissance: {patientInfo.date_de_naissance}</p>
                  <p>Poids: {patientInfo.poids}</p>
                  <p>Taille: {patientInfo.taille}</p>
                  <p>Allergies: {patientInfo.allergies}</p>
                  <p>Type diabète: {patientInfo.type_diabete}</p>
                  <p>Groupe Sanguin: {patientInfo.groupe_sanguin}</p>
                  <button onClick={handleEditClick}>Modifier</button>
                </>
              )}
            </div>
          </div>

          <div label="Consultations">
            <div className="consultations-container">
            {consultations.map((consultation) => (
          <div key={consultation.id} className="consultation">
            <p>Date de consultation: {consultation.date_consultation}</p>
            <p>Heure de consultation: {consultation.heure_consultation}</p>
            <p>Ordonnance: {consultation.ordonnance}</p>
            <p>Description: {consultation.description}</p>
            <p>Bilan: {consultation.bilan}</p>
            <p>Médecin: {consultation.medecin}</p>
            {/* Ajoutez ici d'autres informations de consultation si nécessaire */}
          </div>
            ))}
            </div>
          </div>
        </TabWidget>
      </div>
    </div>
  );
}

export default CarnetMedical;
