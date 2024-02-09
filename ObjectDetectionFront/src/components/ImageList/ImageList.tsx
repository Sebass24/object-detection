import { useEffect, useState } from "react";
import { Button, Container, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Image } from "./image";
import { BsBoxArrowInDown, BsSearch } from "react-icons/bs";

export const ImageList = () => {
  const [images, setImages] = useState<Image[]>([]);
  const [imagePath, setImagePath] = useState<string>("");

  const getImages = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8080/getimages");
      if (!response.ok) {
        throw new Error("Error al obtener las imágenes");
      }
      const data = await response.json();
      setImages(data);
    } catch (error) {
      console.error(error);
    }
  };

  const deleteAll = async () => {
    const confirmacion = window.confirm(
      "¿Estás seguro de que quieres borrar todos los elementos?"
    );

    if (confirmacion) {
      try {
        const response = await fetch("http://127.0.0.1:8080/delete");
        if (!response.ok) {
          throw new Error("Error al eliminar las imágenes");
        }
        setImages([]);
      } catch (error) {
        console.error(error);
      }
    }
  };

  const handleDownloadZip = () => {
    window.location.href = 'http://127.0.0.1:8080/downloadzip';
};

  useEffect(() => {
    getImages();
  }, []);

  return (
    <div className="container-grilla">
      <Container fluid="md" style={{ marginTop: "8rem", marginBottom: "5rem" }}>
        <Table striped bordered className="table table-striped">
          <thead>
            <tr>
              <th>#</th>
              <th>Nombre</th>
              <th>Fecha</th>
              <th>Ver Imagen</th>
            </tr>
          </thead>
          <tbody>
            {images.map((i: Image) => (
              <tr key={images.indexOf(i)}>
                <td>{images.indexOf(i)}</td>
                <td>{i.name}</td>
                <td>{new Date().toDateString()}</td>
                <td>
                  <div style={{ display: "flex" }}>
                    <Link to={`http://127.0.0.1:8080/${i.name}`} style={{ marginRight: "10px" }}>
                      <BsSearch size={26} style={{ cursor: "pointer", color: "black" }} />
                    </Link>
                    <Link to={`http://127.0.0.1:8080/download/${i.name}`} style={{ marginRight: "10px" }}>
                        <BsBoxArrowInDown size={26}  style={{ cursor: "pointer", color: "black" }}/>
                    </Link>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
        <div>
            <Button variant="success" onClick={handleDownloadZip} >
                Descargar Todo
            </Button>
            <Button variant="danger" onClick={deleteAll}>
                Borrar Todo
            </Button>
        </div>
      </Container>
    </div>
  );
};
