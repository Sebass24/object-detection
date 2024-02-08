import { Header } from './components/Header/Header.tsx'
import Footer from './components/Footer/Footer.tsx'
import ImageUpload from './components/ImageUpload/ImageUpload.tsx'
import './App.css'
import { Route, Routes } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {

  return (
    <>
      <Header/>
      <Routes>
        <Route path="/" element= {<ImageUpload/>} />
        <Route path='/imageList' element={<></>} />
      </Routes>
      <Footer/>
    </>
  )
}

export default App
