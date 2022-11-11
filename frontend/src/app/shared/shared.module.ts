import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';

@NgModule({
  providers: [],
  declarations: [],
  imports: [CommonModule, BrowserModule, HttpClientModule, RouterModule],
  exports: [CommonModule, BrowserModule],
})
export class SharedModule {}
