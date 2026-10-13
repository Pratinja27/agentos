import { useEffect, useState } from "react";
import { api } from "./api";
import Layout from "./components/Layout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Goals from "./pages/Goals.jsx";
import Schedule from "./pages/Schedule.jsx";
import Agents from "./pages/Agents.jsx";
import Memory from "./pages/Memory.jsx";
import Approvals from "./pages/Approvals.jsx";

const pages = {
  dashboard: Dashboard,
  goals: Goals,
  schedule: Schedule,
  agents: Agents,
  memory: Memory,
  approvals: Approvals,
};

export default function App() {
  const [page, setPage] = useState("dashboard");
  const [overview, setOverview] = useState(null);

  async function refresh() {
    setOverview(await api.overview());
  }

  useEffect(() => {
    refresh();
  }, [page]);

  const Page = pages[page];
  return (
    <Layout page={page} setPage={setPage} overview={overview}>
      <Page onChange={refresh} />
    </Layout>
  );
}
