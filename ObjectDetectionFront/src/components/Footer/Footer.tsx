import "./Footer.scss";
import Logo from "../Header/Logo/Logo.tsx";

const Footer = () => {
  return (
    <div className="Container_Footer">

      <div className="Container_Footer_contact">
        <span><label style={{ color: "white" }}>Contactanos</label></span>
        <div className="Container_Footer_contact_items">
          <i className="fa-solid fa-location-dot"></i>
          <label>Mendoza-Argentina</label>
        </div>
        <div className="Container_Footer_contact_items">
          <i className="fa-brands fa-whatsapp"></i>
          <label>+54-9-261614011</label>
        </div>
        <div className="Container_Footer_contact_items">
          <i className="fa-solid fa-envelope"></i>
          <label>a.sulia@alumno.um.edu.ar</label>
        </div>
      </div>

      <div className="Logo_Footer">
        <Logo />
      </div>

    </div>
  );
};

export default Footer;