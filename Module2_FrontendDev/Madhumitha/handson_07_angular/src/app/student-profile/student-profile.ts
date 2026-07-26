import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-student-profile',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  template: `
    <div style="padding:40px 32px; max-width:500px; margin:0 auto;">
      <h2>Student Profile</h2>
      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
        <label>Full Name *</label>
        <input formControlName="name" placeholder="Enter your name"
               style="display:block; width:100%; padding:10px; margin:6px 0 16px;
                      border:1px solid #d1dce8; border-radius:6px;" />
        <span style="color:red; font-size:0.85rem;"
              *ngIf="profileForm.get('name')?.touched && profileForm.get('name')?.invalid">
          Name is required
        </span>

        <label>Email *</label>
        <input formControlName="email" type="email" placeholder="Enter your email"
               style="display:block; width:100%; padding:10px; margin:6px 0 16px;
                      border:1px solid #d1dce8; border-radius:6px;" />

        <label>Semester * (1-8)</label>
        <input formControlName="semester" type="number"
               style="display:block; width:100%; padding:10px; margin:6px 0 20px;
                      border:1px solid #d1dce8; border-radius:6px;" />

        <button type="submit" [disabled]="profileForm.invalid"
                style="padding:12px 28px; background:#0f3460; color:#fff;
                       border:none; border-radius:6px; cursor:pointer;">
          Save Profile
        </button>
      </form>
    </div>
  `
})
export class StudentProfileComponent {
  profileForm: FormGroup;
  constructor(private fb: FormBuilder) {
    this.profileForm = this.fb.group({
      name:     ['', Validators.required],
      email:    ['', [Validators.required, Validators.email]],
      semester: ['', [Validators.required, Validators.min(1), Validators.max(8)]],
    });
  }
  onSubmit(): void {
    if (this.profileForm.valid) console.log('Saved:', this.profileForm.value);
  }
}