import React, { useEffect, useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import '../styles/Calendrier.css';
import Agenda from "../images/agenda.png";
import logo from "../images/logo.png";
import Calendrierr from "../images/calendrier.png";
import Calendrier_1 from '../images/calendrier_1.png';
import { useNavigate } from "react-router-dom";
import api from "../api";

const localizer = momentLocalizer(moment);

const eventStyleGetter = (event) => {
  const backgroundColor = '';  
  return {
    style: {
      backgroundColor: backgroundColor,
    },
  };
};

const Calendrier = ({ rendezVousData }) => {
    const navigate = useNavigate();
    console.log("helle" ,rendezVousData);

    const handleAgendaClick = (event) => {
        navigate(`/consultation/${event.id}`);
        console.log("Informations du rendez-vous:", event);
      };

    const handleDeleteRendezVous = (rendezVousId) => {
        confirmAlert({
          title: 'Supprimer le rendez-vous',
          message: 'Êtes-vous sûr de vouloir supprimer ce rendez-vous ?',
          buttons: [
            {
              label: 'Oui, supprimer',
              onClick: () => {
                api.delete(`http://localhost:8000/api/delete/consultations/${rendezVousId}/`)
                  .then(response => {
                    console.log('Rendez-vous deleted successfully:', response.data);
                    // Recharger les rendez-vous après suppression
                    // reloadRendezVous(); // Cette fonction n'est pas définie, vous devez la définir ou la remplacer par une autre logique pour recharger les rendez-vous
                  })
                  .catch(error => console.error('Error deleting rendez-vous:', error));
              },
            },
            {
              label: 'Annuler',
            },
          ],
        });
      };



  return (
    <div className="calendrier-container">
      <h1>Calendrier des rendez-vous</h1>
      <img src={Calendrierr} alt="man" className="doctor" />
      <img src={Calendrier_1} alt="man" className="doctor" />
      <Calendar
        localizer={localizer}
        events={rendezVousData}
        startAccessor="start"
        endAccessor="end"
        eventPropGetter={eventStyleGetter}
        style={{ height: 600 }}
        components={{
          event: (props) => (
            <div>
              <strong>{props.event.title}</strong>
              <img src={Agenda} alt="agenda" className="agenda" onClick={() => handleAgendaClick(props.event)} />
              <div>{props.event.location}</div>
              <button onClick={() => handleDeleteRendezVous(props.event.id)}>Supprimer</button>
              <button onClick={() => handleAgendaClick(props.event)}>Consulter</button>
            </div>
          ),
        }}
      />
    </div>
  );
};

export default Calendrier;
