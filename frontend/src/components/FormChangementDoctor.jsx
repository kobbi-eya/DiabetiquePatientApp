import React, { useState, useEffect } from 'react';
import api from '../api';

import { useParams, useNavigate,Link } from 'react-router-dom';

function ChangeDoctorForm() {
  const [newDoctorEmail, setNewDoctorEmail] = useState('');
  const [notification, setNotification] = useState('');
  const [changeRequests, setChangeRequests] = useState([]);
  const { patientId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    fetchChangeRequests();
  }, [patientId]);

  const fetchChangeRequests = async () => {
    try {
      const response = await api.get(`/api/patients/affichage/change_doctor/${patientId}/`);
      setChangeRequests(response.data);
    } catch (error) {
      console.error('Error fetching change requests:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post(`/api/patients/change_doctor/${patientId}/`, {
        newDoctorEmail: newDoctorEmail
      });
      setNotification('Demande envoyée avec succès.');
      setTimeout(() => {
        setNotification('');
        navigate(`/home_patient/${patientId}`);
      }, 3000); // La notification disparaît après 3 secondes
      console.log(response.data);
    } catch (error) {
      console.error('Error changing doctor:', error);
      // Afficher un message d'erreur à l'utilisateur
    }
  };

  return (
    <div>
      {notification && <div>{notification}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Nouveau médecin (email)"
          value={newDoctorEmail}
          onChange={(e) => setNewDoctorEmail(e.target.value)}
        />
        <button type="submit">Changer de médecin</button>
      </form>

      <h2>Demandes de changement de médecin</h2>
      <table>
        <thead>
          <tr>
            <th>Nouveau Médecin</th>
            <th>État</th>
            <th>Mobile</th>
            <th>nom & prenom</th>
            <th>specialité</th>
          </tr>
        </thead>
        <tbody>
          {changeRequests.map((request) => (
            <tr key={request.id}>
              <td>{request.newDoctorEmail}</td>
              <td>{request.status === 'PENDING' ? 'En attente' : request.status}</td>
              {request.status === 'ACCEPTED' && (
                <>
                  <td>pour prendre un rendez-vous veuillez nous contacter sur {request.newDoctorMobile}</td>
                  <td>{request.newDoctorNom}&{request.newDoctorPrenom}</td>
                  <td>{request.newDoctorSpeciality}</td>

                </>
              )}
            </tr>
          ))}
        </tbody>
      </table>
      <Link to={`/home_patient/${patientId}`} className="btn btn-primary">Retourner à l'accueil</Link>
    </div>
  );
}

export default ChangeDoctorForm;
