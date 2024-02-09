import { Header } from './components/Header/Header.tsx'
import Footer from './components/Footer/Footer.tsx'
import ImageUpload from './components/ImageUpload/ImageUpload.tsx'
import './App.css'
import { Route, Routes } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css';
import { ImageList } from './components/ImageList/ImageList.tsx'

function App() {

  return (
    <>
      <Header/>
      <Routes>
        <Route path="/" element= {<ImageUpload/>} />
        <Route path='/imageList' element={<ImageList/>} />
      </Routes>
      <Footer/>
    </>
  )
}

export default App
