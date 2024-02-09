import React, { useState, ChangeEvent, FormEvent } from "react";
import "./ImageUpload.scss"; 

const Formulario: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadMessage, setUploadMessage] = useState<string>("");
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    setUploadMessage("");
    const selectedFile = event.target.files && event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setUploadMessage("");
    if (file) {
        const formData = new FormData();
        formData.append("request", "");
        formData.append("file", file);
        try {
            const response = await fetch("http://127.0.0.1:8080/", {
                method: "POST",
                body: formData
            });
  
            if (response.ok) {
                setUploadMessage("Archivo subido correctamente");
                console.log("Archivo subido correctamente");
              } else {
                setUploadMessage("Error al subir el archivo: " + response.statusText);
                console.error("Error al subir el archivo:", response.statusText);
              }
        } catch (error) {
            setUploadMessage("Error de red: " + error);
            console.error("Error de red:", error);
        }
      // Aquí puedes implementar la lógica para enviar el archivo y la descripción
      console.log("Archivo:", file);
    
      // Aquí puedes enviar los datos a tu servidor o realizar alguna otra acción
    }
  };

  return (
    <div className="formulario-container">
      <form className="formulario" onSubmit={handleSubmit}>
        <h2>Cargar Foto o Video</h2>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Subir</button>
        {uploadMessage && <p>{uploadMessage}</p>}
      </form>
      
    </div>
  );
};

export default Formulario;