:- discontiguous ciudad/1.
:- discontiguous conexion/3.

ciudad(guatemala).
ciudad(escuintla).
ciudad(mazatenango).
ciudad(quetzaltenango).
ciudad(huehuetenango).
ciudad(coban).
ciudad(peten).
ciudad(jalapa).
ciudad(chiquimula).
ciudad(zacapa).
ciudad(jutiapa).

conexion(guatemala, escuintla, 58).
conexion(guatemala, jalapa, 111).
conexion(guatemala, coban, 212).
conexion(guatemala, zacapa, 148).
conexion(escuintla, mazatenango, 87).
conexion(mazatenango, quetzaltenango, 49).
conexion(quetzaltenango, huehuetenango, 89).
conexion(coban, peten, 359).
conexion(zacapa, chiquimula, 33).
conexion(chiquimula, jutiapa, 137).
conexion(jalapa, jutiapa, 68).

carretera(X, Y, D) :- conexion(X, Y, D).
carretera(X, Y, D) :- conexion(Y, X, D).

ruta(Origen, Destino, Ruta, Distancia) :-
    ruta_aux(Origen, Destino, [Origen], Ruta, Distancia).

ruta_aux(Destino, Destino, Visitados, Visitados, 0).

ruta_aux(Actual, Destino, Visitados, Ruta, Distancia) :-
    carretera(Actual, Siguiente, D1),
    \+ member(Siguiente, Visitados),
    ruta_aux(Siguiente, Destino, [Siguiente|Visitados], RestoRuta, D2),
    Distancia is D1 + D2,
    Ruta = RestoRuta.

ruta_mas_corta(Origen, Destino, MejorRuta, MejorDist) :-
    findall(D-R, ruta(Origen, Destino, R, D), Rutas),
    Rutas \= [],
    min_member(MejorDist-MejorRuta, Rutas).

ciudad(calificacion).
conexion(guatemala, calificacion, 29).