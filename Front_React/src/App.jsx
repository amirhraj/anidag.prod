import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Layout from "./layout/Layout.jsx";
import Profile  from "./pages/Profile/Profile.jsx";
import CarouselComponent from "./components/Carusel/Carusel.jsx";
import Navbar from "./components/Navbar/Navbar_genre.jsx";
// import AnimeListPage from "./components/AnimeCard/AnimeCard.jsx";
import AnimeListPage from "./components/AnimeAnonsCatalog/AnimeAnonsCatalog.jsx"
import Sheduler_section from './components/Sheduler_anime/Sheduler.jsx'
import CardPages from "./components/CardPages/CardPages.jsx";
import SearchResults from "./components/SearchPage/SearchPage.jsx";
import Register from "./pages/Register.jsx";
import VerifyUser from "./pages/VerifyUser.jsx";
import RightsHoldersPolicy from './components/Legal/RightsHoldersPolicy.jsx'
import Terms from './components/Legal/Terms.jsx'
import News from "./components/News/News.jsx";
import AdminPage from "./components/Admin/Admin.jsx";
import NotFoundPage from "./components/NotFoundPage.jsx";
import { useUser } from "./components/UserContext.jsx";

function App() {
  const { userData } = useUser();

  const globalBg = userData?.global_background?.image_url;

  const appStyle = {
    minHeight: "100vh",
    width: "100%",
    ...(globalBg && {
      backgroundImage: `url(https://anidag.ru/api${globalBg.replace(/\\/g, "/")})`,
      backgroundSize: "cover",
      backgroundPosition: "center",
      backgroundRepeat: "no-repeat",
      backgroundAttachment: "fixed",
    }),
  };

  return (
    <div style={appStyle}>
      <Layout>
        <Routes>
          {/* <Route path="/" element={<CarouselComponent />} /> */}
          {/* <Route path="/" element={<Navbar />} /> */}
          <Route path="/" element={<Home />} />
          <Route path="/profile/:username" element={<Profile />} />
          <Route path="/category/:type/:value?" element={<AnimeListPage />} />
          <Route path="/category/schedule" element={<Sheduler_section />} />
          <Route path="/card/:id/:cardType" element={<CardPages />} />
          <Route path="/search/:query" element={<SearchResults />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify/:token" element={<VerifyUser />} />
          <Route path="/RightsHoldersPolicy" element={<RightsHoldersPolicy />} />
          <Route path="/Terms" element={<Terms />} />
          <Route path="/category/news" element={<News />} />
          <Route path="/Adminpanel" element={<AdminPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </div>
  );
}

export default App;




