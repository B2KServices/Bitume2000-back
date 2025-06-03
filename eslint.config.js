module.exports = (async () => {
  const globals = await import("globals");
  const typeScriptEsLintPlugin = await import(
    "@typescript-eslint/eslint-plugin"
  );
  const { FlatCompat } = await import("@eslint/eslintrc");

  const eslint = await import("@eslint/js");

  const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: typeScriptEsLintPlugin.default.configs["recommended"],
  });
  return [
    {
      ...eslint.default.configs.recommended,
      files: ["**/*.ts", "**/*.tsx"],
      languageOptions: {
        sourceType: "commonjs",
        globals: {
          ...globals.node,
        },
      },
    },
    ...compat.config({
      env: { node: true },
      extends: ["plugin:@typescript-eslint/recommended"],
      parser: "@typescript-eslint/parser",
      parserOptions: {
        ecmaVersion: 6,
        sourceType: "commonjs",
      },
      plugins: ["@typescript-eslint"],
      rules: {
        "no-case-declarations": "off",
        "@typescript-eslint/no-explicit-any": "off",
        "@typescript-eslint/no-unused-vars": [
          "error",
          {
            argsIgnorePattern: "^_", // Ignore les arguments qui commencent par _
            varsIgnorePattern: "^_", // Ignore les variables qui commencent par _
          },
        ],
      },
    }),
    {
      files: ["**/*.spec.ts"],
      rules: {
        "no-async-promise-executor": "off",
      },
    },
  ];
})();
