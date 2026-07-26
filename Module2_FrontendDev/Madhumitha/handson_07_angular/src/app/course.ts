import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Course {
  id: number; name: string; code: string; credits: number; grade: string;
}

@Injectable({ providedIn: 'root' })
export class CourseService {
  getCourses(): Observable<Course[]> {
    return new Observable(observer => {
      observer.next([
        { id:1, name:'Data Structures & Algorithms', code:'CS101', credits:4, grade:'A' },
        { id:2, name:'Database Management Systems',  code:'CS102', credits:3, grade:'B' },
        { id:3, name:'Object Oriented Programming',  code:'CS103', credits:4, grade:'A' },
        { id:4, name:'Web Development Fundamentals', code:'CS104', credits:3, grade:'B' },
        { id:5, name:'Python for Data Science',      code:'CS105', credits:4, grade:'A' },
      ]);
      observer.complete();
    });
  }
} {}
