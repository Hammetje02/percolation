/*  Name: Haitham Muhidin
    UvAnetID: 13970356
    Studie: BSc Natuur-en Sterrenkunde; Minor Informtica
    This program is a stack implementation in C. So it facilitates the
    the push, pop, peek and clean functionality of a stack.
*/

#include <stdio.h>
#include <stdlib.h>

#include "stack.h"

/* Handle to stack */
struct stack {
    int *stack_array; // The array which stores the values of the stack
    int top;          // Index of the top of the array/stack
    size_t capacity;  // Maximum amount of elements in stack
    int num_of_push;
    int num_of_pop;
    int max_elements; // The maximum amount of elements the stack contained at
                      // one time
};

/*  Initializes a struct of a stack with a given capacity
    capacity: the maximum amount of element the stack can hold
    Returns:
    a pointer to a stack data structure with a maximum capacity of
    'capacity' if successful, otherwise return NULL.
*/
struct stack *stack_init(size_t capacity) {
    struct stack *s = (struct stack *)malloc(sizeof(struct stack));
    if (s == NULL) {
        return NULL;
    }

    s->stack_array = (int *)malloc(capacity * sizeof(int));
    if (s->stack_array == NULL) {
        free(s);
        return NULL;
    }

    s->capacity = capacity;
    s->num_of_push = 0;
    s->num_of_pop = 0;
    s->max_elements = 0;
    s->top = -1;

    return s;
}

/*  Cleanup stack.
    s: pointer to struct stack which is being freed
*/
void stack_cleanup(struct stack *s) {
    if (s != NULL) {
        free(s->stack_array);
        free(s);
    }
}

/*  Print stack statistics to stderr.
    The format is: 'stats' num_of_pushes num_of_pops max_elements
    s: pointer to struct stack
*/
void stack_stats(const struct stack *s) {
    if (s != NULL) {
        fprintf(stderr, "stats %d %d %d\n", s->num_of_push, s->num_of_pop,
                s->max_elements);
    }
}

/*  Push item onto the stack.
    s: pointer to struct stack
    c: int that is being pushed on stack
    Return 0 if successful, 1 otherwise.
    Side effects:
    if capacity was too small, the new capacity becomes 2 times capacity + 1.
*/
int stack_push(struct stack *s, int c) {
    if (s == NULL) {
        return 1;
    }

    // if the capacity is insufficient, increases the capacity of the stack
    if ((s->top + 1) >= (int)s->capacity) {
        s->stack_array =
            realloc(s->stack_array, 2 * (s->capacity + 1) * sizeof(int));
        if (s->stack_array == NULL) {
            free(s);
            return 1;
        }
        s->capacity = 2 * (s->capacity + 1);
    }

    s->top++;
    s->stack_array[s->top] = c;
    s->num_of_push++;
    if (s->top + 1 > s->max_elements) {
        s->max_elements = s->top + 1;
    }
    return 0;
}

/*  Pop item from stack and return it.
    s: pointer to struct stack
    Returns:
    top item if successful, -1 otherwise. */
int stack_pop(struct stack *s) {
    if (s == NULL || s->top < 0) {
        return -1;
    }

    s->top--;
    s->num_of_pop++;
    return s->stack_array[s->top + 1];
}

/*  Return top of item from stack. Leave stack unchanged.
    s: pointer to struct stack
    Return top item if successful, -1 otherwise.
*/
int stack_peek(const struct stack *s) {
    if (s == NULL || s->top < 0) {
        return -1;
    }
    return s->stack_array[s->top];
}

/*  Checks if the stack contains any elements
    s: pointer to struct stack
    Returns:
    1 if stack is empty, 0 if the stack contains any elements and
    return -1 if the operation fails.
*/
int stack_empty(const struct stack *s) {
    if (s == NULL) {
        return -1;
    }
    if (stack_size(s) == 0) {
        return 1;
    }
    return 0;
}

/*  Gives the number of elements in the stack
    s: pointer to struct stack
    Return:
    the number of elements stored in the stack or 0 if s is NULL
*/
size_t stack_size(const struct stack *s) {
    if (s == NULL) {
        return 0;
    }
    return (size_t)(s->top + 1);
}