const cassandra = require('cassandra-driver');
const readline = require('readline');

// Configuración del cliente
const client = new cassandra.Client({
  contactPoints: ['127.0.0.1'], //IP del nodo de Cassandra
  localDataCenter: 'datacenter1', // Nombre del datacenter 
});

//Función para crear keyspace
async function crearKeyspace(){
  const query = `
    CREATE KEYSPACE IF NOT EXISTS librepost
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
  `;
  try{
    await client.execute(query);
    console.log('Keyspace librepost creado correctamente');
  } catch (error){
    console.error('Error al crear el keyspace:', error);
  }
}

//Función para crear Tabla
async function crearTabla(){
  const query = `
    CREATE TABLE IF NOT EXISTS stamps(
    stamp_id UUID PRIMARY KEY,
    title TEXT,
    country TEXT,
    year INT,
    series TEXT,
    design TEXT,
    face_value FLOAT,
    condition TEXT,
    status TEXT,
    seller TEXT,
    transaction_history LIST<TUPLE<TEXT, TEXT>>,
    tags SET<TEXT>,
    time_value LIST<FROZEN<TUPLE<TEXT, FLOAT>>>
    );
  `;
  try{
    await client.execute('USE librepost');
    await client.execute(query);
    console.log('Tabla stamps creada correctamente');
  } catch (error){
    console.error('Error al crear la tabla:', error);
  }
}

//Función para crear estampillas por defecto
async function crear_estampillas(){
  const query = `
  INSERT INTO stamps (stamp_id, title, country, year, series, design, face_value, condition, status, seller, transaction_history, tags, time_value)
  VALUES (uuid(), 'Estampilla de la Independencia', 'Mexico', 2020, 'Independencia', 'Imagen de la bandera', 5.00, 'nuevo', 'disponible', 'Juan Pérez', [('2024-11-09', 'venta')], {'historia', 'rare'}, [('2024-11-09', 5.00)]);
  `;
  const query2 = `
  INSERT INTO stamps (stamp_id, title, country, year, series, design, face_value, condition, status, seller, transaction_history, tags, time_value)
  VALUES (uuid(), 'Estampilla Bicentenario', 'Chile', 2010, 'Bicentenario', 'Imagen conmemorativa', 10.00, 'dañado', 'disponible', 'Ana López', [('2024-11-09', 'venta')], {'historia', 'bicentenario'}, [('2024-11-09', 10.00)]);
  `;
  const query3 = `
  INSERT INTO stamps (stamp_id, title, country, year, series, design, face_value, condition, status, seller, transaction_history, tags, time_value)
  VALUES (uuid(), 'Estampilla de la Unión Europea', 'Francia', 2004, 'Unión Europea', 'Bandera de la UE con estrellas', 2.00, 'usado', 'disponible', 'Luc Dupont', [('2024-05-10', 'venta')], {'internacional', 'rare'}, [('2024-05-10', 2.00)]);
  `;
  const query4 = `
  INSERT INTO stamps (stamp_id, title, country, year, series, design, face_value, condition, status, seller, transaction_history, tags, time_value)
  VALUES (uuid(), 'Estampilla de la Reina Isabel II', 'Reino Unido', 1953, 'Monarquía', 'Retrato de la Reina Isabel II', 10.00, 'usado', 'vendido', 'Luc Dupont', [('2023-12-01', 'venta'), ('2024-08-15', 'compra')], {'colección', 'historia'}, [('2023-12-01', 10.00), ('2024-08-15', 9.50)]);
  `;
  const query5 = `
  INSERT INTO stamps (stamp_id, title, country, year, series, design, face_value, condition, status, seller, transaction_history, tags, time_value)
  VALUES (uuid(), 'Estampilla del Bicentenario de Argentina', 'Argentina', 2020, 'Bicentenario', 'Retrato de figuras históricas argentinas', 7.50, 'usado', 'disponible', 'Carlos Domínguez', [('2024-03-12', 'venta')], {'historia', 'bicentenario', 'Argentina'}, [('2024-03-12', 7.50)]);
  `;
  try{
    await client.execute(query);
    await client.execute(query2);
    await client.execute(query3);
    await client.execute(query4);
    await client.execute(query5);
    console.log('Estapillas creadas correctamente');
  } catch (error){
    console.error('Error al crear estampillas', error);
  }
}

//Función para limpiar la tabla
async function limpiarTabla() {
  const query = 'TRUNCATE stamps';
  try {
    await client.execute(query);
    console.log('Tabla truncada exitosamente');
  } catch (error) {
    console.error('Error al truncar la tabla:', error);
  }
}

//Instancia para input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

//Función preguntar
function preguntar(pregunta) {
  return new Promise((resolve) => {
      rl.question(pregunta, (respuesta) => {
          resolve(respuesta);
      });
  });
}

async function opciones(){
  console.log("(1) Buscar estampillas por country y year. Filtrando por tags");
  console.log("(2) Encontrar la estampilla mas cara por condicion y anio");
  console.log("(3) Consultar el historial de transacciones de una estampilla especifica");
  console.log("(4) Verificar las estampillas de un vendedor especifico");
  console.log("(5) Buscar por anio y pais. Opcionalmente por Tag y condition");
  console.log("(6) Actualizar registro time_value");
  console.log("(7) Comprar estampilla disponible");
  console.log("(8) Ocupando vista materializada, mostrar las estampillas mas caras");
  console.log("(9) Agregar una estampilla en la base de datos");
  console.log("(10) Ocupando SASI, mostrar las estampillas mas baratas");
  console.log("(11) Salir y limpiar tabla");
}

async function buscar_estampilla(){
  //<--- Variables --->
  const country = await preguntar("Ingrese country: ");
  const year = await preguntar("Ingrese year: ");
  const tag = await preguntar("Ingrese tag: ");
  const query = `
    SELECT * FROM stamps
    WHERE country = ? AND year = ? AND tags CONTAINS ? ALLOW FILTERING;
  `;
  try{
    const result = await client.execute(query, [country, year, tag], { prepare: true });
    //console.log('Estampillas encontradas:', result.rows);1
    result.rows.forEach(row => {
      // Convertir el UUID a una cadena de texto
      const stampId = row.stamp_id.toString();
      const { stamp_id, ...dataWithoutId } = row;
      console.log(`Estampilla encontrada - ID: ${stampId}, Datos:`, dataWithoutId);
    });
  }
  catch (error) {
    console.error('Error al ejecutar la consulta:', error);
  }
}

async function mas_cara(){
  const condition = await preguntar("Ingrese condition: ");
  const year = await preguntar("Ingrese year: ");
  const query = `
    SELECT * FROM stamps 
    WHERE condition = ? AND year = ? ALLOW FILTERING;
  `;
  try {
    const result = await client.execute(query, [condition, year], { prepare: true });
    if (result.rowLength > 0) {
      const mostExpensiveStamp = result.rows.reduce((max, row) => {
        return row.face_value > (max.face_value || 0) ? row : max;
      }, {});
      const stampId = mostExpensiveStamp.stamp_id ? mostExpensiveStamp.stamp_id.toString() : "ID no disponible";
      const { stamp_id, ...dataWithoutId } = mostExpensiveStamp;
      console.log(`La estampilla más cara - ID: ${stampId}, Datos:`, dataWithoutId);
    } else {
      console.log('No se encontraron estampillas con los criterios dados.');
    }
  } catch (error) {
    console.error('Error al ejecutar la consulta:', error);
  }
}

async function historial() {
  const stampId  = await preguntar("Ingrese id: ");
  const query = `
    SELECT transaction_history FROM stamps 
    WHERE stamp_id = ?;
  `;
  try {
    const result = await client.execute(query, [stampId], { prepare: true });
    if (result.rowLength > 0) {
      const transactionHistory = result.rows[0].transaction_history;
      console.log('Historial de transacciones:', transactionHistory);
    } else {
      console.log('No se encontró la estampilla con el ID proporcionado.');
    }
  } catch (error) {
    console.error('Error al ejecutar la consulta:', error);
  }
}

async function verificar() {
  const seller  = await preguntar("Ingrese seller: ");
  const query = `
    SELECT * FROM stamps 
    WHERE seller = ? 
    ALLOW FILTERING
  `;
  try {
    const result = await client.execute(query, [seller], { prepare: true });
    if (result.rowLength > 0) {
      console.log(`Estampillas de ${seller}:`);
      result.rows.forEach(row => {
        console.log(`ID: ${row.stamp_id.toString()}, Título: ${row.title}, Año: ${row.year}, Valor: ${row.face_value}`);
      });
    } else {
      console.log('No se encontraron estampillas para este vendedor.');
    }
  } catch (error) {
    console.error('Error al ejecutar la consulta:', error);
  }
}

async function buscar5() {
  const year = await preguntar("Ingrese year: ");
  const country = await preguntar("Ingrese country: ");
  let params = [year, country];
  let query = `
    SELECT title, stamp_id, status, time_value FROM stamps
    WHERE year = ? AND country = ?
  `; 
  //<--- Tags --->
  let flag = true;
  let otro_tag = "";
  while(flag){
    console.log("Buscar por tags?");
    console.log("(1) Sí");
    console.log("(2) No");
    const desea_tags = await preguntar("Ingrese una opcion: ");
    if(desea_tags == "1"){
      for(let i = 1; i <= 3; i++){
        if(i == 1){
          const tag1 = await preguntar("Ingrese un tag: ");
          query += `AND tags CONTAINS ? `;
          params.push(tag1);
          console.log("Desea buscar por otro tag mas?");
          console.log("(1) Sí");
          console.log("(2) No");
          otro_tag = await preguntar("Ingrese una opcion: ");
          if(otro_tag == "2"){
            break;
          }
        }
        if(i == 2){
          const tag2 = await preguntar("Ingrese un tag: ");
          query += `AND tags CONTAINS ? `;
          params.push(tag2);
          console.log("Desea buscar por otro tag mas?");
          console.log("(1) Sí");
          console.log("(2) No");
          otro_tag = await preguntar("Ingrese una opcion: ");
          if(otro_tag == "2"){
            break;
          }
        }
        if(i == 3){
          const tag3 = await preguntar("Ingrese un tag: ");
          query += `AND tags CONTAINS ? `;
          params.push(tag3);
        }
      }
    }
    flag = false
  }
  //<--- Condition --->
  let flag2 = true;
  while(flag2){
    console.log("Buscar por condition?");
    console.log("(1) Sí");
    console.log("(2) No");
    const desea_condition = await preguntar("Ingrese una opcion: ");
    if(desea_condition == "1"){
      const condition = await preguntar("Ingrese una condition: ");
      query += `
        AND condition = ?
      `;
      params.push(condition);
    }
    flag2 = false;
  }
  query += 'ALLOW FILTERING';
  try {
    const result = await client.execute(query, params, { prepare: true });

    if (result.rowLength > 0) {
      console.log('Resultados de la búsqueda:');
      result.rows.forEach(row => {
        console.log(`ID: ${row.stamp_id.toString()}, Título: ${row.title}, Estado: ${row.status}, Time Value: ${row.time_value}`);
      });
    } else {
      console.log('No se encontraron estampillas que coincidan con los filtros.');
    }
  } catch (error) {
    console.error('Error al ejecutar la consulta:', error);
  }
}

async function time_value() {
  console.log("(1) Agregar time_value");
  console.log("(2) Modificar time_value");
  const modificar = await preguntar("Ingrese una opcion: ");
  const stampId = await preguntar("Ingrese id: ");
  const fecha = await preguntar("Ingrese fecha: ");
  const nuevo_Monto = await preguntar("Ingrese time_value: ");
  if(modificar == "1"){
    const query = `
      UPDATE stamps
      SET time_value = time_value + [?]
      WHERE stamp_id = ?;
    `;
    try {
      await client.execute(query, [[fecha, nuevo_Monto], stampId], { prepare: true });
      console.log(`Nuevo registro agregado a time_value para la estampilla ${stampId}.`);
    } catch (error) {
      console.error('Error al agregar nuevo registro a time_value:', error);
    }
  }
  else if(modificar == "2"){
    const querySELECT = `
      SELECT time_value FROM stamps WHERE stamp_id = ?;
    `;  
    try {
      const result = await client.execute(querySelect, [stampId], { prepare: true });
      if (result.rowLength === 0) {
        console.log('Estampilla no encontrada.');
        return;
      }
      let timeValue = result.rows[0].time_value;
      timeValue = timeValue.map(pair => (pair[0] === fecha ? [fecha, nuevo_Monto] : pair));
      const query = `
        UPDATE stamps
        SET time_value = ?
        WHERE stamp_id = ?;
      `;
      await client.execute(queryUpdate, [timeValue, stampId], { prepare: true });
      console.log(`Registro en time_value modificado.`);
    } catch (error) {
      console.error('Error al modificar registro en time_value:', error);
    }
  }
}

async function comprar() {
  const title = await preguntar("Ingrese title: ");
  const seller = await preguntar("Ingrese seller: ");
  const querySelect = `
    SELECT stamp_id, status, transaction_history 
    FROM stamps 
    WHERE title = ? AND seller = ? ALLOW FILTERING;
  `;
  
  try {
    const result = await client.execute(querySelect, [title, seller], { prepare: true });
    if (result.rowLength === 0) {
      console.log('No se encontró la estampilla con el título y vendedor especificados.');
      return;
    }
    const stamp = result.rows[0];
    if (stamp.status !== 'disponible') {
      console.log('La estampilla no está disponible para la compra.');
      return;
    }
    if (!stamp.transaction_history) {
      stamp.transaction_history = [];
    }
    // Obtener la fecha actual
    const fechaCompra = new Date().toISOString().split('T')[0];
    1
    // Convertir la nueva transacción en una tupla
    const { Tuple } = require('cassandra-driver').types;
    const nuevaTransaccion = new Tuple(fechaCompra, 'compra');

    // Agregar la nueva transacción como una tupla
    stamp.transaction_history.push(nuevaTransaccion);
    // Realizar la transacción de compra
    const batchQuery = `
      BEGIN BATCH
        UPDATE stamps SET status = 'vendido' WHERE stamp_id = ?;
        UPDATE stamps SET seller = 'D' WHERE stamp_id = ?;
        UPDATE stamps SET transaction_history = ? WHERE stamp_id = ?;
      APPLY BATCH;
    `;
    await client.execute(batchQuery, [stamp.stamp_id, stamp.stamp_id, stamp.transaction_history, stamp.stamp_id], { prepare: true });
    console.log('Estampilla comprada exitosamente.');
  } catch (error) {
    console.error('Error al intentar comprar la estampilla:', error);
  }
}

async function view() {
  //<--- Crear vista materializada --->
  const queryView = `
    CREATE MATERIALIZED VIEW IF NOT EXISTS most_expensive_stamp_by_condition AS
    SELECT stamp_id, title, country, year, face_value, condition, status, time_value
    FROM stamps
    WHERE condition IS NOT NULL AND stamp_id IS NOT NULL
    PRIMARY KEY (condition, stamp_id);
  `;
  try {
    await client.execute(queryView);
    console.log("Vista materializada creada correctamente.");
  } catch (error) {
    console.error("Error al crear la vista materializada:", error);
    return;
  }
  //<--- Buscar la más cara ---> 
  const year = await preguntar("Ingrese year: ");
  const queryNuevo = `
    SELECT stamp_id, title, face_value 
    FROM most_expensive_stamp_by_condition 
    WHERE condition = 'nuevo' AND year = ? ALLOW FILTERING;
  `;
  try {
    const result = await client.execute(queryNuevo, [year], { prepare: true });
    if (result.rowLength > 0) {
      const mostExpensiveStamp = result.rows.reduce((max, row) => {
        return row.face_value > (max.face_value || 0) ? row : max;
      }, {});
      const stampId = mostExpensiveStamp.stamp_id ? mostExpensiveStamp.stamp_id.toString() : "ID no disponible";
      const { stamp_id, ...dataWithoutId } = mostExpensiveStamp;
      console.log(`La estampilla más cara en condición "nuevo" para el año ${year} es: ID: ${stampId}, Datos:`, dataWithoutId);
    } else {
      console.log(`No se encontraron estampillas en condición "nuevo" para el año ${year}.`);
    }
  } catch (error) {
    console.error('Error al obtener la estampilla más cara:', error);
  }
  const queryUsado = `
    SELECT stamp_id, title, face_value 
    FROM most_expensive_stamp_by_condition 
    WHERE condition = 'usado' AND year = ? ALLOW FILTERING;
  `;
  try {
    const result = await client.execute(queryUsado, [year], { prepare: true });
    if (result.rowLength > 0) {
      const mostExpensiveStamp = result.rows.reduce((max, row) => {
        return row.face_value > (max.face_value || 0) ? row : max;
      }, {});
      const stampId = mostExpensiveStamp.stamp_id ? mostExpensiveStamp.stamp_id.toString() : "ID no disponible";
      const { stamp_id, ...dataWithoutId } = mostExpensiveStamp;
      console.log(`La estampilla más cara en condición "usado" para el año ${year} es: ID: ${stampId}, Datos:`, dataWithoutId);
    } else {
      console.log(`No se encontraron estampillas en condición "usado" para el año ${year}.`);
    }
  } catch (error) {
    console.error('Error al obtener la estampilla más cara:', error);
  }
  const queryDanio = `
    SELECT stamp_id, title, face_value 
    FROM most_expensive_stamp_by_condition 
    WHERE condition = 'dañado' AND year = ? ALLOW FILTERING;
  `;
  try {
    const result = await client.execute(queryDanio, [year], { prepare: true });
    if (result.rowLength > 0) {
      const mostExpensiveStamp = result.rows.reduce((max, row) => {
        return row.face_value > (max.face_value || 0) ? row : max;
      }, {});
      const stampId = mostExpensiveStamp.stamp_id ? mostExpensiveStamp.stamp_id.toString() : "ID no disponible";
      const { stamp_id, ...dataWithoutId } = mostExpensiveStamp;
      console.log(`La estampilla más cara en condición "dañado" para el año ${year} es: ID: ${stampId}, Datos:`, dataWithoutId);
    } else {
      console.log(`No se encontraron estampillas en condición "dañado" para el año ${year}.`);
    }
  } catch (error) {
    console.error('Error al obtener la estampilla más cara:', error);
  }
}

async function agregar() {
  const title = await preguntar("Ingrese title: ");
  const country = await preguntar("Ingrese country: ");
  const year = await preguntar("Ingrese year: ");
  const series = await preguntar("Ingrese series: ");
  const design = await preguntar("Ingrese desing: ");
  const face_value = await preguntar("Ingrese face_value: ");
  const condition = await preguntar("Ingrese condition: ");
  const status = await preguntar("Ingrese status: ");
  const seller = await preguntar("Ingrese seller: ");
  let flag = true;
  let tags = [];
  while(flag){
    console.log("(1) agregar un tag");
    console.log("(2) no agregar más tags");
    let quiere_tag = await preguntar("Ingrese su opcion: ");
    if(quiere_tag == "1"){
      let tag = await preguntar("Ingrese tag: ");
      tags.push(tag);
    }
    else if(quiere_tag == "2"){
      flag = false;
    }
  }

  const query = `
  INSERT INTO stamps (stamp_id, title, country, year, series, design, face_value, condition, status, seller, transaction_history, tags, time_value)
  VALUES (uuid(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;

  try{
    await client.execute(query, [title, country, year, series, design, face_value, condition, status, seller, [], tags, []], { prepare: true });
    console.log('Estampilla añadida con éxito');
  } catch (error) {
    console.error('Error al añadir la estampilla:', error);
  }
}

async function mas_barata() {
  //<--- Indice SASI --->
  const createYearIndexQuery = `
    CREATE CUSTOM INDEX IF NOT EXISTS ON stamps(year) 
    USING 'org.apache.cassandra.index.sasi.SASIIndex' 
    WITH OPTIONS = {
      'mode': 'PREFIX'
    };
  `;
  const createStatusIndexQuery = `
  CREATE CUSTOM INDEX IF NOT EXISTS ON stamps(status) 
  USING 'org.apache.cassandra.index.sasi.SASIIndex';
  `;
  try {
    await client.execute(createYearIndexQuery);
    console.log("Índice SASI para 'year' creado con éxito.");

    await client.execute(createStatusIndexQuery);
    console.log("Índice SASI para 'status' creado con éxito.");
  } catch (error) {
    console.error("Error al crear los índices SASI:", error);
  }
  //<--- Busqueda --->
  const startYear = await preguntar("Ingrese el primer year: ")
  const endYear = await preguntar("Ingrese el ultimo year: ")
  const query = `
    SELECT stamp_id, title, face_value, status, year 
    FROM stamps 
    WHERE year >= ? AND year <= ? 
    ALLOW FILTERING
  `;
  try {
    const result = await client.execute(query, [startYear, endYear], { prepare: true });
    // Agrupar las estampillas por 'status'
    const groupedByStatus = result.rows.reduce((acc, row) => {
      // Si el status no existe en el acumulador, lo agregamos
      if (!acc[row.status]) {
        acc[row.status] = [];
      }
      acc[row.status].push(row);
      return acc;
    }, {});
    // Iterar sobre cada grupo de 'status' y encontrar la estampilla más barata
    for (const status in groupedByStatus) {
      if (groupedByStatus[status].length > 0) {
        // Ordenar las estampillas de este estado por `face_value` en orden ascendente
        const cheapestStamp = groupedByStatus[status]
          .sort((a, b) => a.face_value - b.face_value)[0];
  
        // Mostrar la estampilla más barata para este estado
        console.log(`Para el estado "${status}":`);
        console.log(`  Stamp ID: ${cheapestStamp.stamp_id.toString()}, Title: ${cheapestStamp.title}, Price: ${cheapestStamp.face_value}, Year: ${cheapestStamp.year}`);
      } else {
        console.log(`No se encontraron estampillas para el estado "${status}".`);
      }
    }
  } catch (error) {
    console.error('Error al ejecutar la consulta:', error);
  }
}

async function main() {
  try{
    //<--- Conexión --->
    await client.connect();
    console.log('Conectado a Cassandra');
    await crearKeyspace();
    await crearTabla();
    await crear_estampillas();
    //<--- Menú --->
    let flag = true;
    let opcion = "0";
    while(flag){
      opciones();
      //<--- Input --->
      opcion = await preguntar("Ingrese su opción: ");
      //<--- Opciones --->
      if(opcion == "1"){
        await buscar_estampilla();
      }
      else if(opcion == "2"){
        await mas_cara();
      }
      else if(opcion == "3"){
        await historial();
      }
      else if(opcion == "4"){
        await verificar();
      }
      else if(opcion == "5"){
        await buscar5();
      }
      else if(opcion == "6"){
        await time_value();
      }
      else if(opcion == "7"){
        await comprar();
      }
      else if(opcion == "8"){
        await view();
      }
      else if(opcion == "9"){
        await agregar();
      }
      else if(opcion == "10"){
        await mas_barata();
      }
      else if(opcion == "11"){
        flag = false;
        await limpiarTabla();
      }
    }

  }catch (error) {
    console.error('Error al conectarte a Cassandra:', error);
  }finally {
    console.log("Conexion con la BD cerrada.")
    await client.shutdown(); //Cerrar la conexión
  }
}

main();