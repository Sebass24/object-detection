import { useEffect, useState } from "react";
import { Container, Table } from "react-bootstrap";
import { Link } from "react-router-dom";



export const ImageList = () => {
    const [images, setImages] = useState<string[]>([]);
    
    const getImages = async () => {
        try {
            const response = await fetch('URL_DE_TU_ENDPOINT');
            if (!response.ok) {
              throw new Error('Error al obtener las imágenes');
            }
            const data = await response.json();
            setImages(data);
        }
        catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
      getImages();
    }, []); 

    
    return (
        <>  
        <div className='productContainer'>
            <Container fluid="md">
                <Table striped bordered className="contacts-table-abm" >
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Imagen</th>
                            <th>Nombre</th>
                            <th>Detalle</th>
                        </tr>
                    </thead>
                    <tbody>
                        {images.map((i: string) => (
                            <tr key={i}>
                                
                            </tr>
                        ))}
                    </tbody>
                </Table >
            </Container>
        </div>
        </>
    )
};
