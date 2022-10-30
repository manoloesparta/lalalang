import logo from "../assets/logo.png";
import title from "../assets/title.png";

function Banner() {
  return (
    <div className="columns">
      <div className="column is-full">
        <img src={title} width="500px" />
        <img src={logo} width="100px" />
      </div>
    </div>
  );
}

export default Banner;
