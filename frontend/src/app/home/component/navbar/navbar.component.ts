import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  borderSelected = 'background-color: #254E7A';
  mediaQuery: boolean = true;
  items: MenuItem[] = [];
  url = '';

  width: MediaQueryList = window.matchMedia('(min-width: 768px)');

  constructor(private router: Router) {
    setInterval(() => {
      if (this.width.matches) {
        this.mediaQuery = true;
      } else {
        this.mediaQuery = false;
      }
    }, 3000);
  }

  ngOnInit(): void {
    this.url = this.router.url;
    this.items = [
      {
        label: 'Data flow',
        icon: 'pi pi-home',
        routerLink: '/',
      },

      {
        label: 'Filtering',
        icon: 'pi pi-filter',
        routerLink: '/filter',
      },

      {
        label: 'Importation',
        icon: 'pi pi-upload',
        routerLink: '/importation',
      },
    ];
  }
}
