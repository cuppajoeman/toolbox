#include <stddef.h>

#ifndef DYNAMIC_ARRAY_H
#define DYNAMIC_ARRAY_H

typedef struct {
  void **storage;
  size_t used;
  size_t length;
  size_t elem_size;
} DynamicArray;

#endif

void init_darray(DynamicArray *a, size_t initial_length, size_t elem_size);
void insert_darray(DynamicArray *a, void *element);
void free_darray(DynamicArray *a);
void at(DynamicArray *a, void *elem_ptr, size_t i);
