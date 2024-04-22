import React from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/login"
import Register from "./pages/Register"
import HomeMedecin from "./pages/HomeMedecin"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import RegisterPatient from "./pages/RegisterPatient"
import CreateRv from "./pages/CreateRv"
import axios from 'axios';

axios.defaults.withCredentials = true;

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

//function RegisterAndLogout() {
  //localStorage.clear()
  //return <Register />
//}


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <HomeMedecin />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/login/registerpatient/:medecinId" element={<RegisterPatient />} />
        <Route path="/login/CreateRv/:medecinId" element={<CreateRv />} />
        <Route path="/login/home_medecin/:medecinId" element={<HomeMedecin />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App