import { BrowserRouter, Route, Routes } from "react-router-dom";

import DashboardPage from "./pages/DashboardPage";
import PredictionDetailsPage from "./pages/PredictionDetailsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/predictions/:predictionId" element={<PredictionDetailsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;