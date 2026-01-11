import { useEffect } from "react";
import { UseFormReturn } from "react-hook-form";

export const useAutoDismissErrors = (formMethods: UseFormReturn<any>) => {
  const { formState: { errors }, clearErrors } = formMethods;

  useEffect(() => {
    if (Object.keys(errors).length > 0) {
      const timer = setTimeout(() => {
        clearErrors();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [errors, clearErrors]);
};