// Importez les dépendances nécessaires
import React, { useState, useEffect } from 'react';
import api from '../api';
import { useParams } from 'react-router-dom';
import moment from 'moment';
function DoctorChangeRequests() {
  const [changeRequests, setChangeRequests] = useState([]);
  const [patientsInfo, setPatientsInfo] = useState({}); // État pour stocker les informations des patients
  const { medId } = useParams();

  useEffect(() => {
    const fetchChangeRequests = async () => {
      try {
        const response = await api.get(`http://localhost:8000/api/doctor/change_requests/${medId}/`);
        setChangeRequests(response.data.changeRequests);
        
        // Récupérez les informations de chaque patient
        const patientsInfoData = {};
        for (const request of response.data.changeRequests) {
          const patientId = request.patient; // Supposons que request.id contient l'ID du patient
          const patientInfoResponse = await api.get(`http://localhost:8000/api/patients/${patientId}/`);
          patientsInfoData[patientId] = patientInfoResponse.data; // Stockez les informations du patient par son ID
        }
        setPatientsInfo(patientsInfoData); // Mettez à jour l'état avec les informations des patients
      } catch (error) {
        console.error('Error fetching change requests:', error);
      }
    };
    fetchChangeRequests();
  }, [medId]);

  const handleAcceptRequest = async (requestId) => {
    try {
      const response = await api.post(`/api/doctor/change_requests/${requestId}/accept/`);
      console.log(response.data);
      // Mettre à jour l'interface ou afficher un message de succès
    } catch (error) {
      console.error('Error accepting change request:', error);
      // Afficher un message d'erreur à l'utilisateur
    }
  };

  const handleRejectRequest = async (requestId) => {
    try {
      const response = await api.post(`/api/doctor/change_requests/${requestId}/reject/`);
      console.log(response.data);
      // Mettre à jour l'interface ou afficher un message de succès
    } catch (error) {
      console.error('Error rejecting change request:', error);
      // Afficher un message d'erreur à l'utilisateur
    }
  };

  return (
    <div>
      <h2>Demandes de changement de médecin</h2>
      <table>
        <thead>
          <tr>
            <th>Patient</th>
            <th>Date de Demande</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {changeRequests.map((request) => (
            <tr key={request.id}>
              <td>
                {patientsInfo[request.patient] ? `${patientsInfo[request.patient].prenom} ${patientsInfo[request.patient].nom} (${patientsInfo[request.patient].email})` : 'Chargement...'}
              </td>
              <td>{moment(request.date_requested).format('DD/MM/YYYY HH:mm:ss')}</td> 
              <td>
                <button onClick={() => handleAcceptRequest(request.id)}>Accepter</button>
                <button onClick={() => handleRejectRequest(request.id)}>Rejeter</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DoctorChangeRequests;
