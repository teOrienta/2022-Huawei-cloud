import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MenuModule } from 'primeng/menu';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { CalendarModule } from 'primeng/calendar';
import { SliderModule } from 'primeng/slider';
import { SelectButtonModule } from 'primeng/selectbutton';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { DialogModule } from 'primeng/dialog';
import { SkeletonModule } from 'primeng/skeleton';
import { AccordionModule } from 'primeng/accordion';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MenuModule,
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SkeletonModule,
    SelectButtonModule,
    InputTextModule,
    DropdownModule,
    DialogModule,
    AutoCompleteModule,
  ],
  exports: [
    MenuModule,
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SkeletonModule,
    SelectButtonModule,
    InputTextModule,
    DropdownModule,
    DialogModule,
    AutoCompleteModule,
    AccordionModule,
  ],
})
export class PrimeComponentsModule {}
