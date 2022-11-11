import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  borderSelected = 'background-color: #254E7A';
  url = '';
  constructor(private router: Router) {}

  ngOnInit(): void {
    this.url = this.router.url;
  }
}
