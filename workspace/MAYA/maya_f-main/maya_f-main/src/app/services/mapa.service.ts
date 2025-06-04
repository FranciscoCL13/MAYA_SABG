import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { from, Observable } from 'rxjs';
import { environment } from '../../environments/environment';

import * as L from 'leaflet';

@Injectable({
  providedIn: 'root'
})
export class MapaService {

  apiUrl = environment.sofiaApiUrl;

  public readonly anpmxLayer: L.Layer = L.geoJSON(); // Define la capa.
  private readonly combinedLayerGroup: L.FeatureGroup = L.featureGroup();

  constructor(private http: HttpClient) { }

  public getMetadataOptions(): Observable<any> {
    return this.http.get(`${this.apiUrl}/mapas/metadata`);
  }

  public getMapa(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/mapas/layer/${id}`);
  }

  public getMapaEje(): Observable<any> {
    return this.http.get(`${this.apiUrl}/mapas/layer/t7_eje`);
  }

  public getMapaCadena(): Observable<any> {
    return this.http.get('/assets/geojson_jsonb_cadea.json');
  }

  public getAreas(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/mapas/areas/${id}`);
  }

  toggleAnpmxLayer(add: boolean): void {
    if (add) {
      if (!this.combinedLayerGroup.hasLayer(this.anpmxLayer)) {
        // this.combinedLayerGroup.addLayer(this.anpmxLayer);
        alert('entraste en if');
      }
    } else {
      if (this.combinedLayerGroup.hasLayer(this.anpmxLayer)) {
        alert('entraste en else');
        // this.combinedLayerGroup.removeLayer(this.anpmxLayer);
      }
    }
  }

}
