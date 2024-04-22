// Calendrier.jsx

import React, { useEffect, useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import '../styles/Calendrier.css';
import Agenda from "./agenda.png";
import logo from "./logo.png";
import Calendrierr from "./calendrier.png";
import Calendrier_1 from './calendrier_1.png'; // Importez les événements

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
    console.log("helle" ,rendezVousData)
    const handleAgendaClick = (event) => {
        // Vous pouvez ajouter ici la logique pour ouvrir une fenêtre modale ou rediriger vers la page des informations du rendez-vous
        console.log("Informations du rendez-vous:", event);
        // Par exemple, pour rediriger vers une page spécifique avec les informations du rendez-vous, vous pouvez utiliser le navigateur
        //window.location.href = `/rendezvous/${event.id}`; // Assurez-vous d'adapter cette URL à votre structure de route
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
          event: (props) => {
            return (
              <div>
                <strong>{props.event.title}</strong>
                <img src={Agenda} alt="agenda" className="agenda" onClick={() => handleAgendaClick(props.event)}   />
                <div>{props.event.location}</div>
              </div>
            );
          },
        }}
      />
    </div>
  );
};

export default Calendrier;
