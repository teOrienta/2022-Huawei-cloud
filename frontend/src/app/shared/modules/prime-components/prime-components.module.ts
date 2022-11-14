import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { CalendarModule } from 'primeng/calendar';
import { SliderModule } from 'primeng/slider';
import { SelectButtonModule } from 'primeng/selectbutton';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { DialogModule } from 'primeng/dialog';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SelectButtonModule,
    InputTextModule,
    DropdownModule,
    DialogModule,
    AutoCompleteModule,
  ],
  exports: [
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SelectButtonModule,
    InputTextModule,
    DropdownModule,
    DialogModule,
    AutoCompleteModule,
  ],
})
export class PrimeComponentsModule {}
