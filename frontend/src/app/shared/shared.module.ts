import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { PrimeComponentsModule } from './modules/prime-components/prime-components.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  providers: [],
  declarations: [],
  imports: [
    CommonModule,
    BrowserModule,
    HttpClientModule,
    RouterModule,
    PrimeComponentsModule,
    BrowserAnimationsModule,
  ],
  exports: [
    CommonModule,
    BrowserModule,
    PrimeComponentsModule,
    FormsModule,
    ReactiveFormsModule,
  ],
})
export class SharedModule {}
