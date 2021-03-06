find_package(X11 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(VTK)
find_package(GTK2)
find_package(CGAL REQUIRED COMPONENTS Core)
find_package(GNUGTS REQUIRED)
find_package(CImg REQUIRED)
find_package(MySQL)
find_package(MySQLpp REQUIRED)
find_package(GLIB2)
set(Boost_USE_STATIC_LIBS   OFF)
set(Boost_USE_MULTITHREADED ON)
find_package(Boost 1.38 COMPONENTS system regex filesystem thread python)
find_package(F2C REQUIRED)
find_package(Plot REQUIRED)
find_package(Gnuplot REQUIRED)
find_package(MPFR)
find_package(GMP)
find_package(SQLITE3 REQUIRED)
find_package(MPI)
find_package(Arpack REQUIRED)
find_package(ArpackPP REQUIRED)
find_package(Petsc)
find_package(LAPACK REQUIRED)
find_package(BLAS REQUIRED)
find_package(SuperLU REQUIRED)
find_package(BerkeleyDB REQUIRED)
find_package(METIS REQUIRED)
find_package(TCL REQUIRED)
find_package(MED REQUIRED)
find_package(ORACLE)
find_package(PythonLibs REQUIRED)
