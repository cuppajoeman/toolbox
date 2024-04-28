#include "dynamic_array.h"
#include <stdlib.h>
#include <string.h>

void init_darray(DynamicArray *a, size_t initial_length, size_t elem_size) {
  a->elem_size = elem_size;
  a->storage = malloc(initial_length * elem_size);
  a->used = 0;
  a->length = initial_length;
}

void insert_darray(DynamicArray *a, void *element) {
    // a->used is the number of used entries, because a->storage[a->used++] updates a->used only *after* the array has been accessed.
    // Therefore a->used can go up to a->size 
    if (a->used == a->length) {
        a->length *= 2;
        a->storage = realloc(a->storage, a->length * a->elem_size);
    }
    a->storage[a->used++] = element;
}
    
void free_darray(DynamicArray *a) {
  free(a->storage);
  a->storage = NULL;
  a->used = a->length = 0;
}

void at(DynamicArray *a, void *elem_ptr, size_t i) {
  // stores the pointer to the element you are looking for in elem_ptr
  // a->storage + i is pointer arithmetic which allows us to access the ith element
  memcpy(elem_ptr, a->storage + i, a->elem_size);
}
