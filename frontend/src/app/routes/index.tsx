import { createBrowserRouter } from "react-router-dom";
import { ProtectedRoute } from "./ProtectedRoute";
import { Layout } from "@/widgets/Layout";
import { LoginPage } from "@/features/auth/pages/LoginPage";
import { RegisterPage } from "@/features/auth/pages/RegisterPage";
import { DashboardPage } from "@/features/dashboard/pages/DashboardPage";
import { SitesPage } from "@/features/sites/pages/SitesPage";
import { CamerasPage } from "@/features/cameras/pages/CamerasPage";
import { AlertLogsPage } from "@/features/alerts/pages/AlertLogsPage";
import { AlertThresholdsPage } from "@/features/alerts/pages/AlertThresholdsPage";
import { AIModelsPage } from "@/features/ai/pages/AIModelsPage";
import { TrainingJobsPage } from "@/features/ai/pages/TrainingJobsPage";
import { DatasetsPage } from "@/features/ai/pages/DatasetsPage";
import { InspectionPage } from "@/features/inspection/pages/InspectionPage";
import {
  DataAugmentPage,
  DataCleanPage,
  DataCollectionEnvPage,
  DataCollectionJobsPage,
} from "@/features/prototype/pages/DataCollectionPrototypePages";
import {
  AiEvaluationPage,
  AiTrainingPage,
  DataInspectionPage,
} from "@/features/prototype/pages/InspectionAiPrototypePages";
import {
  AlertHistoryPage,
  MonitoringDashboardPage,
  MonitoringSiteDetailPage,
  UnauthorizedAlertPage,
} from "@/features/prototype/pages/MonitoringAlertPrototypePages";
import {
  MesIntegrationPage,
  WorkerFlowPage,
} from "@/features/prototype/pages/WorkerMesPrototypePages";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <Layout />,
        children: [
          { path: "/", element: <MonitoringDashboardPage /> },
          { path: "/dashboard", element: <DashboardPage /> },
          {
            path: "/mornitoring/dashboard",
            element: <MonitoringDashboardPage />,
          },
          {
            path: "/mornitoring/:siteId",
            element: <MonitoringSiteDetailPage />,
          },
          { path: "/sites", element: <SitesPage /> },
          { path: "/cameras", element: <CamerasPage /> },
          { path: "/data-collection/env", element: <DataCollectionEnvPage /> },
          {
            path: "/data-collection/jobs",
            element: <DataCollectionJobsPage />,
          },
          { path: "/data-collection/clean", element: <DataCleanPage /> },
          { path: "/data-collection/augment", element: <DataAugmentPage /> },
          { path: "/data-inspection", element: <DataInspectionPage /> },
          { path: "/alerts/logs", element: <AlertLogsPage /> },
          { path: "/alerts/thresholds", element: <AlertThresholdsPage /> },
          { path: "/alerts/unauthorized", element: <UnauthorizedAlertPage /> },
          { path: "/alerts/history", element: <AlertHistoryPage /> },
          { path: "/ai/models", element: <AIModelsPage /> },
          { path: "/ai/training-jobs", element: <TrainingJobsPage /> },
          { path: "/ai/training", element: <AiTrainingPage /> },
          { path: "/ai/datasets", element: <DatasetsPage /> },
          { path: "/ai/evaluation", element: <AiEvaluationPage /> },
          { path: "/inspection", element: <InspectionPage /> },
          { path: "/worker-flow", element: <WorkerFlowPage /> },
          { path: "/mes-integration", element: <MesIntegrationPage /> },
        ],
      },
    ],
  },
]);
