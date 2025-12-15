import js from "@eslint/js";
import globals from "globals";
import tsParser from "@typescript-eslint/parser";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import prettier from "eslint-plugin-prettier";

export default [
  js.configs.recommended,
  {
    ignores: ["dist/**", "node_modules/**"],
  },
  {
    files: ["**/*.ts"],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: 2020,
      sourceType: "module",
      globals: { ...globals.node, ...globals.es2023 },
      parserOptions: {
        project: true,
      },
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      prettier,
    },
    rules: {
      ...tsPlugin.configs.recommended.rules,
      "no-case-declarations": "off",
      "@typescript-eslint/no-empty-object-type": "warn",
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unsafe-function-type": "warn",
      "@typescript-eslint/ban-ts-comment": "off",
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "no-console": "error",
      camelcase: "warn",
    },
  },
  {
    files: ["**/*.{spec,test}.ts"],
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.jest,
        ...globals.mocha,
        ...globals.chai,
      },
    },
    rules: {
      "no-async-promise-executor": "off",
    },
  },
];
