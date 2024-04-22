import api from "../api";
import React, { useEffect, useState } from "react";
const getPatientInfo = (patientId) => {
    return api.get(`/api/patients/${patientId}`)
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching patient info:', error);
        return null;
      });
  };
  export default getPatientInfo
  