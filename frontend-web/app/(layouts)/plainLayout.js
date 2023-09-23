import NavBar from "../Components/navbar";
import Footer from "../Components/footer";


function Layout({ children, showNavBar, justifyCenter }) {
  return (
    <div>
      <div className="bg-white min-h-screen flex flex-col">
        <NavBar />
        <div className=" mx-auto flex flex-col justify-center text-center">
          {children}
        </div>
        <Footer />
      </div>
    </div>
  );
}

export default Layout;