import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [],
  templateUrl: './spinner.component.html',
  styleUrl: './spinner.component.css'
})
export class SpinnerComponent implements OnInit {

  @Input()
  public loading: boolean;

  constructor() {
    this.loading = false;
  }

  ngOnInit() {
  }

  public mostrar() {
    this.loading = true;
  }

  public ocultar() {
    this.loading = false;
  }

}

