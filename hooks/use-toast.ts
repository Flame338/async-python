"use client"

import type { ToastAction } from "@/components/ui/toast"

import * as React from "react"
import * as ToastPrimitives from "@radix-ui/react-toast"

const TOAST_LIMIT = 1
const TOAST_REMOVE_DELAY = 1000000

type ToastsMap = Map<
  string,
  {
    toast: ToastPrimitives.ToastProps
    timeout: ReturnType<typeof setTimeout>
  }
>

type ToastType = ToastPrimitives.ToastProps & {
  id: string
  title?: React.ReactNode
  description?: React.ReactNode
  action?: React.ReactElement<typeof ToastAction>
}

type ActionType =
  | {
      type: "ADD_TOAST"
      toast: ToastType
    }
  | {
      type: "UPDATE_TOAST"
      toast: Partial<ToastType>
    }
  | {
      type: "DISMISS_TOAST"
      toastId?: string
    }
  | {
      type: "REMOVE_TOAST"
      toastId?: string
    }

interface State {
  toasts: ToastType[]
}

const toastTimeouts = new Map<string, ReturnType<typeof setTimeout>>()

const addToRemoveQueue = (toastId: string) => {
  if (toastTimeouts.has(toastId)) {
    return
  }

  const timeout = setTimeout(() => {
    toastTimeouts.delete(toastId)
    dispatch({
      type: "REMOVE_TOAST",
      toastId: toastId,
    })
  }, TOAST_REMOVE_DELAY)

  toastTimeouts.set(toastId, timeout)
}

const reducer = (state: State, action: ActionType): State => {
  switch (action.type) {
    case "ADD_TOAST":
      return {
        ...state,
        toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
      }

    case "UPDATE_TOAST":
      return {
        ...state,
        toasts: state.toasts.map((t) => (t.id === action.toast.id ? { ...t, ...action.toast } : t)),
      }

    case "DISMISS_TOAST":
      const { toastId } = action
      // ! Side effects !
      if (toastId) {
        addToRemoveQueue(toastId)
      } else {
        state.toasts.forEach((toast) => {
          addToRemoveQueue(toast.id)
        })
      }

      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === toastId || toastId === undefined
            ? {
                ...t,
                open: false,
              }
            : t,
        ),
      }
    case "REMOVE_TOAST":
      if (action.toastId === undefined) {
        return {
          ...state,
          toasts: [],
        }
      }
      return {
        ...state,
        toasts: state.toasts.filter((t) => t.id !== action.toastId),
      }
  }
}

const listeners: ((state: State) => void)[] = []

let globalState: State = {
  toasts: [],
}

function dispatch(action: ActionType) {
  globalState = reducer(globalState, action)
  listeners.forEach((listener) => listener(globalState))
}

type ToastOptions = Partial<ToastType>

function useToast() {
  const [toasts, setToasts] = React.useState(globalState.toasts)

  React.useEffect(() => {
    const listener = (state: State) => {
      setToasts(state.toasts)
    }

    listeners.push(listener)
    return () => {
      const index = listeners.indexOf(listener)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    }
  }, [toasts])

  return {
    ...ToastPrimitives,
    toasts: toasts,
    toast: React.useCallback((props: ToastOptions) => {
      const id = `toast-${Math.random().toString(36).substring(2, 9)}`

      const update = (props: ToastOptions) =>
        dispatch({
          type: "UPDATE_TOAST",
          toast: { ...props, id },
        })
      const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id })

      dispatch({
        type: "ADD_TOAST",
        toast: {
          ...props,
          id,
          open: true,
          onOpenChange: (open) => {
            if (!open) {
              dismiss()
            }
          },
        },
      })

      return {
        id: id,
        update,
        dismiss,
      }
    }, []),
    dismiss: React.useCallback((toastId?: string) => {
      dispatch({ type: "DISMISS_TOAST", toastId })
    }, []),
  }
}

export { useToast }
