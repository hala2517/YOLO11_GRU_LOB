import { RouterProvider } from "react-router-dom";
import { QueryProvider } from "@/app/providers/QueryProvider";
import { ThemeProvider } from "@/app/providers/ThemeProvider";
import { router } from "@/app/routes";
import { Toaster } from "sonner";

function App() {
  return (
    <ThemeProvider defaultTheme="dark">
      <QueryProvider>
        <RouterProvider router={router} />
        <Toaster richColors position="top-right" />
      </QueryProvider>
    </ThemeProvider>
  );
}

export default App;
