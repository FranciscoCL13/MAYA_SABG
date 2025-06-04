import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DropdownModule } from 'primeng/dropdown';
import { MapaService } from '../../services/mapa.service';
import * as L from 'leaflet';
import { FormsModule } from '@angular/forms';
import { SpinnerComponent } from '../../common/spinner/spinner.component';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { MultiSelectModule } from 'primeng/multiselect';
import { CheckboxModule } from 'primeng/checkbox';

@Component({
  selector: 'app-mapa',
  standalone: true,
  imports: [CommonModule, SpinnerComponent, FormsModule, DropdownModule, MultiSelectModule, InputTextModule, ButtonModule, CheckboxModule],
  templateUrl: './mapa.component.html',
  styleUrl: './mapa.component.css'
})
export class MapaComponent implements OnInit {
  // @ViewChild('layers', { static: false }) layersRef!: ElementRef<HTMLDivElement>;
  @ViewChild('legend', { static: false }) legendRef!: ElementRef<HTMLDivElement>;
  /**
   * Referencia al spinner.
   */
  @ViewChild('spinner', { static: true }) public spinner !: SpinnerComponent;

  expedienteBuscado: string = '';  // Variable para almacenar el expediente ingresado

  isAnpmxLayerVisible: boolean = false; // Estado del checkbox
  private map!: L.Map;
  private zoomControlElement: HTMLElement | null = null;
  private marcadorExpediente!: L.Marker | null;
  result: string = '';
  style_tmp: string = '';

  // inicio de nuevo
  private anpmxLayer!: L.Layer; // Capa ANPMX.
  // fin nuevo

  private readonly combinedLayerGroup: L.FeatureGroup = L.featureGroup(); // Inicialización como variable de clase

  lat = 18.50;
  lng = -89.70;
  zoom = 8;

  // inicio de nuevo
  metadata_options =  [
    { label: "Tramo 1", value: 1, color: '#FFC107' },
    { label: "Tramo 2", value: 2, color: '#00BCD4' },
    { label: "Tramo 3", value: 3, color: '#FF5722' },
    { label: "Tramo 4", value: 4, color: '#9C27B0' },
    { label: "Tramo 4-2", value: 5, color: '#4CAF50' },
    { label: "Tramo 5", value: 6, color: '#FFEB3B' },
    { label: "Tramo 6", value: 7, color: '#795548' },
    { label: "Tramo 6-2", value: 8, color: '#00796B' },
    { label: "Tramo 7", value: 9, color: '#E040FB' },
    { label: "Tramo 7-2", value: 10, color: '#616161' }    
  ];
  // fin de nuevo

  selectedOptions: any[] = []; // Almacena las opciones seleccionadas

  cartodbAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>';

  icon = {
    icon: L.icon({
      iconSize: [25, 41],
      iconAnchor: [13, 0],
      iconUrl: 'assets/images/marker-icon.png',
      shadowUrl: 'assets/images/marker-shadow.png'
    })
  };

  constructor(
    private mapaService: MapaService,    
  ) { }

  ngOnInit(): void {

    this.selectedOptions = [...this.metadata_options];
    
    this.map = L.map('map', {
      center: [this.lat, this.lng],
      zoom: this.zoom,
      zoomControl: false  // Desactiva el control de zoom predeterminado
    });

    L.control.zoom({ position: 'topright' }).addTo(this.map);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: this.cartodbAttribution
    }).addTo(this.map);


    // Crear un control personalizado para mostrar el nivel de zoom
    const zoomLevelControl = L.Control.extend({
      options: { position: 'topright' },
      onAdd: () => {
        // Crear el elemento HTML para mostrar el nivel de zoom
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom icon-button');
        container.style.cursor = 'pointer';
        // container.style.padding = '8px';
        container.style.backgroundColor = 'white';
        // container.style.borderRadius = '4px';
        // container.innerHTML = `<strong>Zoom: ${this.zoom}</strong>`; // Nivel de zoom inicial en negrita
        container.innerHTML = `<strong>${this.zoom}</strong>`; // Nivel de zoom inicial en negrita

        // Guardar el elemento para poder actualizarlo después
        this.zoomControlElement = container;

        return container;
      }
    });

    // Agregar el control personalizado al mapa
    this.map.addControl(new zoomLevelControl());

    // Actualizar el nivel de zoom mostrado cada vez que el usuario hace zoom
    this.map.on('zoomend', () => {
      const currentZoom = this.map.getZoom();      
      if (this.zoomControlElement) {
        this.zoomControlElement.innerHTML = `&nbsp;&nbsp;<strong>${currentZoom}</strong>&nbsp;&nbsp;`;
      }
      this.toggleLegendVisibility();
      this.updateLayerStyles(currentZoom);
    });

    this.map.on('move', () => this.clearResult());
    this.map.on('zoom', () => this.clearResult());

    // Crear el botón de refresh
    const refreshControl = L.Control.extend({
      options: { position: 'topright' },
      onAdd: () => {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom icon-button');
        container.innerHTML = '<i class="pi pi-refresh"></i>'; // Ícono de PrimeNG
        container.style.cursor = 'pointer';
        // container.style.padding = '8px';
        container.style.backgroundColor = 'white';
        // container.style.borderRadius = '4px';

        // Manejar el clic en el botón de refresh
        container.onclick = () => this.refreshMap();

        return container;
      }
    });

    // Agregar el control de refresh al mapa
    this.map.addControl(new refreshControl());

    // iniciar data
    this.initMap();
    // this.loadDataLayers();    

    // Inicializar la visibilidad de la leyenda    
    this.toggleLegendVisibility();
  // abajo llave que cierra el ngoninit    
    this.checkLayerStatus();
  }

  // Método de refresh para recargar los datos en el mapa
  refreshMap() {
    // Restablecer la vista del mapa a las coordenadas iniciales y zoom
    this.clearAllLayers();
    this.map.setView([this.lat, this.lng], this.zoom);

    this.initMap();

    if (this.marcadorExpediente) {
      this.map.removeLayer(this.marcadorExpediente);
    }
  }

  toggleLegendVisibility() {
    let zoomm = this.map.getZoom();
    // Ocultar o mostrar la leyenda dependiendo del nivel de zoom
    if (zoomm > 13) {
      this.legendRef.nativeElement.style.display = 'block';      
    } else {
      this.legendRef.nativeElement.style.display = 'none';
    }

    // if (zoomm >= 7 && zoomm <=12 ) {
    //   this.layersRef.nativeElement.style.display = 'block';
    // } else{
    //     this.layersRef.nativeElement.style.display = 'none';
    // }
  }

  

  private loadDataLayers(): void {
    let zoom = this.map.getZoom();    
    this.spinner.mostrar();
    this.selectedOptions = [...this.metadata_options];    
    const capas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; // IDs de tus capas
    capas.forEach((capaId, index) => {
      this.mapaService.getMapa(capaId).subscribe((data: any) => {
        const layer = L.geoJSON(data, {
          style: (feature) => this.getPolygonStyle(zoom, feature),
          onEachFeature: (feature, layer) => {
            // Agregar evento de clic al polígono
            layer.on('click', () => {
              this.showPopupWithDetails(feature, layer);
            });
          }

        });

      // Asignar el ID a cada capa para poder filtrarlas
      (layer as any).capaId = capaId;
  
        // Agregar la capa al grupo combinado
        this.combinedLayerGroup.addLayer(layer);
        this.centerMapOnGroup(); // Centrar el mapa en el grupo
        this.combinedLayerGroup.addTo(this.map); // Añadir el grupo al mapa
        // this.spinner.ocultar();
      });
    });
  }



  // Métodos para manipular las capas
  removeSpecificLayer(layer: L.Layer): void {
    this.combinedLayerGroup.removeLayer(layer); // Elimina una capa específica
  }

  clearAllLayers(): void {
    // Contar capas antes de eliminar
    // const initialLayerCount = this.combinedLayerGroup.getLayers().length;

    // Limpiar todas las capas dentro del grupo
    this.combinedLayerGroup.clearLayers();

    // Remover el grupo completo del mapa para asegurarse de que desaparezcan las capas
    this.map.removeLayer(this.combinedLayerGroup);

    // Verificar el número de capas dentro del grupo después de limpiar
    // const finalLayerCount = this.combinedLayerGroup.getLayers().length;
  }

  private centerMapOnGroup(): void {
    // Verifica si el grupo tiene capas antes de centrar el mapa
    if (this.combinedLayerGroup.getLayers().length > 0) {
      this.map.fitBounds(this.combinedLayerGroup.getBounds());
    }
  }
  
  getPolygonStyle(zoom: number, feature: any) {

    const name_layer = feature.capa;
    const regimen = feature?.properties?.['REGIMEN DE PROPIEDAD'];
    let color = '';    
    let fillColor = '';
    let fillOpacity = 1;
    let opacity= 1;
    let weight = 0;
    let zoom_actual = 0;
    let setear_poligonos = false;
    let setear_capas = false;
    zoom_actual = zoom;

    if (zoom_actual > 0 && zoom_actual <= 13 ){
      setear_poligonos = true;
    }
    if (zoom_actual > 13 && zoom_actual < 20 ){
      setear_capas = true;
    }

    if(setear_poligonos){
      this.style_tmp = 'poligonos'
      weight = 5;
      return this.return_style_poligonos(color, fillColor, fillOpacity, name_layer, opacity, weight);
    } else if (setear_capas){
      this.style_tmp = 'capas'
      weight = 1;
      return this.return_style_capas(color, fillColor, fillOpacity, name_layer, opacity, weight, regimen);
    }else {
      return {      
        color: color,   // Borde del polígono
        weight: weight,          // Grosor del borde
        opacity: 1,         // Opacidad del borde
        fillColor: fillColor, // Color de relleno según el régimen
        fillOpacity: fillOpacity
      };
    }
    

  }

  // funcion que para al hacer click muestre info
  // addGeoJsonLayer(data: any) {
  //   let zoom = this.map.getZoom();
  //   // Ejemplo de datos GeoJSON
  //   const geoJsonData = data;

  //   // Agregar al mapa evento de clic en cada polígono
  //   L.geoJSON(geoJsonData, {
  //     style: (feature) => this.getPolygonStyle(zoom, feature),
  //     onEachFeature: (feature, layer) => {
  //       // Agrega un evento de clic al polígono
  //       layer.on('click', () => {
  //         this.showPopupWithDetails(feature, layer);
  //       });
  //     }
  //   }).addTo(this.map);
  // }

  showPopupWithDetails(feature: any, layer: L.Layer) {
    // Obtiene las propiedades de la característica
    const properties = feature.properties;

    const consecutivo = properties?.['gid'] || 'Desconocido';
    const expediente = properties?.['expediente'] || 'N/A';
    const entidad = properties?.['ENTIDAD'] || 'N/A';
    const municipio = properties?.['MUNICIPIO'] || 'N/A';
    const localidad = properties?.['LOCALIDAD'] || 'N/A';
    const regimen = properties?.['REGIMEN DE PROPIEDAD'] || 'N/A';
    const titular_ant = properties?.['TITULAR ANTERIOR'] || 'N/A';
    const adquirente = properties?.['ADQUIRENTE\nFONATUR/FTM'] || 'N/A';
    const estatus_proc = properties?.['ESTATUS PROCESAL'] || 'N/A';
    
    // Crea el contenido del popup
    const popupContent = `
      <div>
      <strong>Consecutivo: </strong> ${consecutivo}<br>
      <strong>Expediente: </strong> ${expediente}<br>
      <strong>Entidad: </strong> ${entidad}<br>
      <strong>Municipio: </strong> ${municipio}<br>
      <strong>Localidad: </strong> ${localidad}<br>
      <strong>Regimen de propiedad: </strong> ${regimen}<br>
      <strong>Titular anterior: </strong> ${titular_ant}<br>
      <strong>Adquiriente FONATUR/FTM: </strong> ${adquirente}<br>
      <strong>Estatus procesal: </strong> ${estatus_proc}<br>
      </div>
    `;

    // Muestra el popup en el polígono seleccionado
    layer.bindPopup(popupContent).openPopup();
  }

  buscarPorExpediente(): void {
    let encontrado = false; // Variable para verificar si se encontró el expediente
    // Verificar si el grupo de capas tiene capas (geojson)
    this.combinedLayerGroup.eachLayer((layer: L.Layer) => {
      const geoJsonLayer = layer as L.GeoJSON;
      geoJsonLayer.eachLayer((featureLayer: L.Layer) => {
        const properties = (featureLayer as any).feature?.properties;
        
        if (properties && properties.expediente === this.expedienteBuscado) {
          encontrado = true; 
          // Ajusta el mapa al área del polígono encontrado
          const bounds = (featureLayer as L.GeoJSON).getBounds();
          this.map.fitBounds(bounds);

          // Calcula el centro de los límites del polígono
          const center = bounds.getCenter();

          // Elimina el marcador anterior si existe
          if (this.marcadorExpediente) {
            this.map.removeLayer(this.marcadorExpediente);
          }

          // Crea y agrega un nuevo marcador en el centro del polígono
          this.marcadorExpediente = L.marker(center, {
            icon: L.icon({
              iconUrl: 'assets/images/marker-icon.png', // Ruta al ícono del marcador
              iconSize: [25, 41],
              iconAnchor: [13, 41]
            })
          }).addTo(this.map);
        }
      });
    });

    if (!encontrado) {
      this.result = `No se encontró ningún polígono expediente: ${this.expedienteBuscado}`
    }else{
      this.result = `Se encontró polígono expediente: ${this.expedienteBuscado}`
    }

    this.expedienteBuscado = ''

  }

  clearResult(): void {
    this.result = ''; // Limpiar el mensaje de resultado
  }

  filtrarCapas(): void {
    let pre_select = this.isAnpmxLayerVisible;
    this.isAnpmxLayerVisible = false;
    this.clearAllLayers(); // Limpia las capas actuales
    let zoom = this.map.getZoom();    
    

    // this.toggleAnpmxLayer(false);
    let numero_capas = this.selectedOptions.length;
    if(numero_capas !== 0){
      this.spinner.mostrar();
    }
    
    // this.clearAllLayers(); // Limpia las capas actuales

    // Recorrer cada opción seleccionada y cargar la capa correspondiente
    this.selectedOptions.forEach((option) => {

      if(option.value == 1 || option.value == 2 || option.value == 3 || option.value ==4 || option.value == 5 || option.value == 6 || 
        option.value == 7 || option.value == 8 || option.value == 9 || option.value ==10){
          this.mapaService.getMapa(option.value).subscribe((data: any) => {
            const layer = L.geoJSON(data, {
              style: (feature) => this.getPolygonStyle(zoom, feature),
              onEachFeature: (feature, layer) => {
                // Agregar evento de clic al polígono
                layer.on('click', () => {
                  this.showPopupWithDetails(feature, layer);
                });
              }
            });
    
            // Agrega la capa al grupo de capas
            this.combinedLayerGroup.addLayer(layer);
            this.combinedLayerGroup.addTo(this.map);
    
            // Ajusta el mapa para mostrar todas las capas cargadas
            this.map.fitBounds(this.combinedLayerGroup.getBounds());
            this.spinner.ocultar();
          });      
        } 

        


    });

    if(pre_select){
      console.dir('habilitadooooooooooooooooooooooooo');
    } else {
      console.dir('DESHABILITADO');
    }
  }

  // Función para actualizar el estilo de todas las capas en combinedLayerGroup
  updateLayerStyles(zoom: number) {
    this.combinedLayerGroup.eachLayer((layer: any) => {
      if (layer.setStyle) {  // Verifica que la capa tenga el método setStyle
        layer.setStyle((feature: any) => this.getPolygonStyle(zoom, feature));
      }
    });
  }
  
  return_style_poligonos(color: any, fillColor: any, fillOpacity: any, name_layer:any, opacity:any, weight: number){
    if(name_layer == 'Tramo 1'){
      color = '#FFC107';        //ROSA BORDE
      fillColor= '#FFC107';
      opacity = 1;
    }
    if(name_layer == 'Tramo 2'){
        color = '#00BCD4';   // CYAN BORDE
        fillColor = '#00BCD4'; // 
    }
    if(name_layer == 'Tramo 3'){
        color = '#FF5722';   // ROJO BORDE
        fillColor = '#FF5722'; // Color de relleno según el régimen
    }
    if(name_layer == 'Tramo 4'){
        color = '#9C27B0';   // MORADO BORDE
        fillColor = '#9C27B0'; // Color de relleno según el régimen
    }
    if(name_layer == 'Tramo 4-2'){
        color = '#4CAF50';   // VERDE - BORDE
        fillColor = '#4CAF50'; // Color de relleno según el régimen
    }
    if(name_layer == 'Tramo 5'){
        color = '#FFEB3B';   // AMARILLO BORDE
        fillColor = '#FFEB3B'; // Color de relleno según el régimen
    }
    if(name_layer == 'Tramo 6'){
      color = '#795548';   // blue dark
      fillColor = '#795548'; // Color de relleno según el régimen
    }
    if(name_layer == 'Tramo 6-2'){
      color = '#00796B';   // cafe oscuro
      fillColor = '#00796B'; // Color de relleno según el régimen
    }
    if(name_layer == 'Tramo 7'){
      color = '#E040FB';   // gris claro
      fillColor = '#E040FB'; // Color de relleno según el régimen
    }
    if(name_layer == 'Tramo 7-pend'){
      color = '#616161';   // grid oscuro
      fillColor = '#616161'; // Color de relleno según el régimen
    }
    if(name_layer == 'anpmx.shp'){
      color = '#212121';    //color del borde de la linea
      fillColor = '#B3E5FC';    
      fillOpacity = 0.40;  //transparencia del relleno (entre menor grado, menos visible el color del relleno)
      opacity = 1; //0 = transparente
      weight = 1;
    }

    return {      
      color: color,   // Borde del polígono
      weight: weight,          // Grosor del borde
      opacity: opacity,         // Opacidad del borde
      fillColor: fillColor, // Color de relleno según el régimen
      fillOpacity: fillOpacity
    };
  }

  return_style_capas(color: any, fillColor: any, fillOpacity: any, name_layer:any, opacity:any, weight: number, regimen: string){
    
    // Asignar color según el régimen de propiedad
    if (regimen === 'PROPIEDAD PUBLICA' || 
      regimen === 'PROPIEDAD PUBLICA ' || 
      regimen === 'Propiedad Pública' || 
      regimen === 'Propiedad pública' || 
      regimen === 'PUBLICA' || 
      regimen === 'Bien Público' || 
      regimen === 'Pública') {
      fillColor = '#4CAF50'; // Verde para propiedad PUBLICA
      color = '#4CAF50';
    } else if (regimen === 'PROPIEDAD PRIVADA' || 
      regimen === 'PROPIEDAD PRIVADA ' || 
      regimen === 'Propiedad privada' || 
      regimen === 'PRIVADA' || 
      regimen === 'Propiedad Privada' || 
      regimen === 'propiedad privada ') {
      fillColor = '#FFC107'; // Amarillo para propiedad PRIVADA
      color = '#FFC107';
    } else if (regimen === 'PROPIEDAD SOCIAL' || 
      regimen ==='PROPIEDAD SOCIAL ' || 
      regimen ==='Propiedad social' || 
      regimen ==='Propiedad social ' || 
      regimen === 'Propiedad Social' || 
      regimen === 'Social' || 
      regimen === 'SOCIAL') {
        fillColor = '#2196F3'; // Azul para propiedad comunal
        color = '#2196F3';
    } else if (regimen === 'TERRENOS NACIONALES' || 
      regimen === 'TERRENOS NACIONALES ' || 
      regimen === 'Terrenos Nacionales' || 
      regimen === 'Terrenos Nacionales ' || 
      regimen === 'TERRENOS NACIONAL' || 
      regimen === 'TERRENOS NACIONAL ' || 
      regimen ==='TERRENO NACIONAL ' || 
      regimen === 'TERRENO NACIONAL' || 
      regimen === 'Terreno Nacional' || 
      regimen === 'Baldío / Terreno Nacional') {
        fillColor = '#D32F2F'; // Rojo
        color ='#D32F2F';
    } else if (regimen === 'FEDERAL' || 
      regimen === 'Zona Federal') {
        fillColor = '#7C4DFF'; // MORADO
        color = '#7C4DFF';
      } else if (regimen === 'FUNDO LEGAL') {
        fillColor = '#00BCD4'; // 
        color = '#00BCD4';
      } else if (regimen === 'Posesionario') {
        fillColor = '#E91E63'; // 
        color = '#E91E63';
      } else if(name_layer == 'anpmx.shp'){
        color = '#212121';    //color del borde de la linea
        fillColor = '#B3E5FC';    
        fillOpacity = 0.40;  //transparencia del relleno (entre menor grado, menos visible el color del relleno)
        opacity = 1; //0 = transparente
        weight = 1;

      } else {
        console.dir('no entro a opcion');
    }

    return {      
      color: color,   // Borde del polígono
      weight: weight,          // Grosor del borde
      opacity: 0,         // Opacidad del borde
      fillColor: fillColor, // Color de relleno según el régimen
      fillOpacity: fillOpacity
    };
  }

  getAreasStyle(feature: any) {

    const name_layer = feature.capa;    

    let color = '#212121';    //color del borde de la linea
    let fillColor = '#B3E5FC';    
    let fillOpacity = 0.55;  //transparencia del relleno (entre menor grado, menos visible el color del relleno)
    let opacity= 0; //0 = transparente
    let weight = 1;
      
    return this.return_style_areas(color, fillColor, fillOpacity, name_layer, opacity, weight);

  }

  return_style_areas(color: any, fillColor: any, fillOpacity: any, name_layer:any, opacity:any, weight: number){

    return {      
      color: color,   // Borde del polígono
      weight: weight,          // Grosor del borde
      opacity: 1,       // Opacidad del borde
      fillColor: fillColor, // Color de relleno según el régimen
      fillOpacity: fillOpacity
    };
  }

  initMap(){
    // Carga las capas.
    this.loadDataLayers();
    this.loadDataAreasNatu(true); // Cambia el parámetro si necesitas agregar o no.
  }

  /**
   * Carga las áreas naturales protegidas.
   * @param addLayer Indica si se deben agregar las capas.
   */
  private loadDataAreasNatu(addLayer: boolean): void {
    const capas = [11];
    // this.spinner.mostrar();
  
    capas.forEach((capaId) => {
      this.mapaService.getMapa(capaId).subscribe((data: any) => {
        const layer = this.createLayer(data, capaId);
  
        if (addLayer) {
          this.addLayerToGroup(layer);
          this.isAnpmxLayerVisible = true; // Marcar el checkbox como seleccionado.
        } else {
          this.removeLayerFromGroup(capaId);
          this.isAnpmxLayerVisible = false; // Desmarcar el checkbox.
        }
        this.spinner.ocultar();
      });
    });
  }

  private createLayer(data: any, capaId: number): L.Layer {
    const layer = L.geoJSON(data, {
      style: (feature) => this.getAreasStyle(feature),
    });
  
    // Asignar un identificador único a la capa.
    (layer as any).capaId = capaId;

  // Si el capaId corresponde al de anpmxLayer, asignarlo a this.anpmxLayer.
  if (capaId === 11) {
    this.anpmxLayer = layer;
    console.log('anpmxLayer inicializado:', this.anpmxLayer);
  }
  
    return layer;
  }

  private addLayerToGroup(layer: L.Layer): void {
    this.combinedLayerGroup.addLayer(layer);
    this.combinedLayerGroup.addTo(this.map); // Asegurar que el grupo esté en el mapa.
    this.isAnpmxLayerVisible = true;
    console.log('Capa agregada al grupo. isAnpmxLayerVisible =', this.isAnpmxLayerVisible);
  }
  
  /**
   * Elimina una capa del grupo combinado por su ID.
   */
  private removeLayerFromGroup(capaId: number): void {
    this.combinedLayerGroup.eachLayer((existingLayer: any) => {
      if (existingLayer.capaId === capaId) {
        this.combinedLayerGroup.removeLayer(existingLayer);
        console.log('Capa eliminada del grupo:', capaId);
      }
    });
  
    this.isAnpmxLayerVisible = false;
    console.log('isAnpmxLayerVisible =', this.isAnpmxLayerVisible);
  }

  /**
   * Maneja el cambio del checkbox.
   */
  onCheckboxChange(event: any): void {
    this.isAnpmxLayerVisible = event.checked;
    // Llama a toggleAnpmxLayer con el estado actual.
    this.toggleAnpmxLayer(this.isAnpmxLayerVisible);
  }

  toggleAnpmxLayer(add: boolean): void {

    if (!this.anpmxLayer) {
      console.error('Error: anpmxLayer no está inicializado.');
      return;
    }
  
    if (add) {
      if (!this.combinedLayerGroup.hasLayer(this.anpmxLayer)) {
        this.combinedLayerGroup.addLayer(this.anpmxLayer);
        console.log('Capa ANPMX agregada al grupo.');
      } else {
        console.log('La capa ANPMX ya está en el grupo.');
      }
    } else {
      if (this.combinedLayerGroup.hasLayer(this.anpmxLayer)) {
        console.log('unoooooooo Capas en combinedLayerGroup:', this.combinedLayerGroup.getLayers());
        this.combinedLayerGroup.removeLayer(this.anpmxLayer);
        console.log('Capa ANPMX eliminada del grupo.');
        console.log('doooooooooos en combinedLayerGroup:', this.combinedLayerGroup.getLayers());
      } else {
        console.log('La capa ANPMX no estaba en el grupo.');
      }
    }
  }

/**
 * Verifica si la capa ANPMX está presente en el mapa.
 */
private checkLayerStatus(): void {
  const capas = [11];
  let layerExists = false;

  this.combinedLayerGroup.eachLayer((existingLayer: any) => {
    if (capas.includes(existingLayer.capaId)) {
      layerExists = true;
    }
  });

  this.isAnpmxLayerVisible = layerExists; // Actualiza el estado del checkbox.
}

}   // esta llave  cierra export (todo)
