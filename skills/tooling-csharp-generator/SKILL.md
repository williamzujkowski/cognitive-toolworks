---
name: "C# .NET Tooling Specialist"
slug: "tooling-csharp-generator"
description: "Generate C# .NET project scaffolding with dotnet CLI, xUnit/NUnit, StyleCop analyzers, and packaging (NuGet/Docker)."
capabilities:
  - Project structure generation (library, console, web-api, blazor, wpf, maui)
  - Build tool setup (dotnet CLI, MSBuild, solution files)
  - Testing framework configuration (xUnit, NUnit, MSTest, Moq)
  - Code quality tools (StyleCop, Roslyn analyzers, SonarAnalyzer)
  - Packaging and distribution (NuGet, Docker, native AOT)
  - ASP.NET Core setup (minimal APIs, MVC, Blazor)
inputs:
  - project_type: "library | console | web-api | blazor | wpf | maui (string)"
  - dotnet_version: "6.0 | 7.0 | 8.0 (string)"
  - test_framework: "xunit | nunit | mstest (string)"
  - project_name: "Name of the project (string)"
outputs:
  - project_structure: "Directory layout with all config files (JSON)"
  - csproj_file: "Complete .csproj configuration"
  - solution_file: ".sln file for multi-project solutions"
  - test_project: "Test project configuration"
keywords:
  - csharp
  - dotnet
  - tooling
  - nuget
  - xunit
  - aspnet
  - blazor
  - roslyn
  - msbuild
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://learn.microsoft.com/en-us/dotnet/core/
  - https://learn.microsoft.com/en-us/aspnet/core/
  - https://xunit.net/docs/getting-started/netcore/
  - https://learn.microsoft.com/en-us/nuget/
  - https://github.com/DotNetAnalyzers/StyleCopAnalyzers
---

## Purpose & When-To-Use

**Trigger conditions:**
- Starting a new C# .NET project requiring modern tooling
- Creating ASP.NET Core web APIs or Blazor applications
- Building cross-platform console applications or libraries
- Setting up .NET MAUI mobile applications
- Creating NuGet packages for distribution
- Migrating .NET Framework projects to .NET Core/5+

**Not for:**
- Legacy .NET Framework 4.x projects (use older MSBuild templates)
- Unity game development (use Unity's project templates)
- Xamarin projects (migrated to .NET MAUI)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `project_type` must be one of: library, console, web-api, blazor, wpf, maui
- `dotnet_version` must be one of: 6.0, 7.0, 8.0
- `test_framework` must be one of: xunit, nunit, mstest
- `project_name` must be valid .NET identifier (PascalCase recommended)

**Source freshness:**
- .NET docs must be accessible [accessed 2025-10-26](https://learn.microsoft.com/en-us/dotnet/core/)
- ASP.NET Core docs must be accessible [accessed 2025-10-26](https://learn.microsoft.com/en-us/aspnet/core/)
- xUnit docs must be accessible [accessed 2025-10-26](https://xunit.net/docs/getting-started/netcore/)
- NuGet docs must be accessible [accessed 2025-10-26](https://learn.microsoft.com/en-us/nuget/)

---

## Procedure

### T1: Basic Project Structure (≤2k tokens)

**Fast path for common cases:**

1. **Directory Layout Generation**
   ```
   ProjectName/
     src/
       ProjectName/
         ProjectName.csproj
         Class1.cs
     tests/
       ProjectName.Tests/
         ProjectName.Tests.csproj
         UnitTest1.cs
     ProjectName.sln
     .gitignore
     README.md
   ```

2. **Core .csproj** [accessed 2025-10-26](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview)
   ```xml
   <Project Sdk="Microsoft.NET.Sdk">
     <PropertyGroup>
       <TargetFramework>net8.0</TargetFramework>
       <Nullable>enable</Nullable>
       <ImplicitUsings>enable</ImplicitUsings>
       <LangVersion>latest</LangVersion>
     </PropertyGroup>

     <ItemGroup>
       <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556">
         <PrivateAssets>all</PrivateAssets>
         <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
       </PackageReference>
     </ItemGroup>
   </Project>
   ```

3. **Solution File** (.sln)
   ```
   Microsoft Visual Studio Solution File, Format Version 12.00
   Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "ProjectName", "src\ProjectName\ProjectName.csproj", "{GUID}"
   EndProject
   Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "ProjectName.Tests", "tests\ProjectName.Tests\ProjectName.Tests.csproj", "{GUID}"
   EndProject
   ```

**Decision:** If only basic scaffolding needed → STOP at T1; otherwise proceed to T2.

---

### T2: Full Tooling Setup (≤6k tokens)

**Extended configuration with testing and web frameworks:**

1. **Testing Framework Configuration**

   **xUnit** [accessed 2025-10-26](https://xunit.net/docs/getting-started/netcore/)
   ```xml
   <Project Sdk="Microsoft.NET.Sdk">
     <PropertyGroup>
       <TargetFramework>net8.0</TargetFramework>
       <IsPackable>false</IsPackable>
       <IsTestProject>true</IsTestProject>
     </PropertyGroup>

     <ItemGroup>
       <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.9.0" />
       <PackageReference Include="xunit" Version="2.7.0" />
       <PackageReference Include="xunit.runner.visualstudio" Version="2.5.7">
         <PrivateAssets>all</PrivateAssets>
         <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
       </PackageReference>
       <PackageReference Include="Moq" Version="4.20.70" />
       <PackageReference Include="FluentAssertions" Version="6.12.0" />
       <PackageReference Include="coverlet.collector" Version="6.0.0">
         <PrivateAssets>all</PrivateAssets>
         <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
       </PackageReference>
     </ItemGroup>

     <ItemGroup>
       <ProjectReference Include="..\..\src\ProjectName\ProjectName.csproj" />
     </ItemGroup>
   </Project>
   ```

   **NUnit** (alternative) [accessed 2025-10-26](https://docs.nunit.org/)
   ```xml
   <ItemGroup>
     <PackageReference Include="NUnit" Version="4.1.0" />
     <PackageReference Include="NUnit3TestAdapter" Version="4.5.0" />
     <PackageReference Include="NUnit.Analyzers" Version="4.1.0" />
   </ItemGroup>
   ```

2. **Code Quality and Analyzers**

   **StyleCop + Roslyn Analyzers** [accessed 2025-10-26](https://github.com/DotNetAnalyzers/StyleCopAnalyzers)
   ```xml
   <ItemGroup>
     <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556">
       <PrivateAssets>all</PrivateAssets>
       <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
     </PackageReference>
     <PackageReference Include="SonarAnalyzer.CSharp" Version="9.23.0.88079">
       <PrivateAssets>all</PrivateAssets>
       <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
     </PackageReference>
   </ItemGroup>
   ```

   .editorconfig:
   ```ini
   # Top-most EditorConfig file
   root = true

   [*.cs]
   # Code style rules
   dotnet_sort_system_directives_first = true
   csharp_style_var_for_built_in_types = true
   csharp_style_var_when_type_is_apparent = true

   # Naming conventions
   dotnet_naming_rule.interfaces_should_be_prefixed_with_i.severity = warning
   dotnet_naming_rule.interfaces_should_be_prefixed_with_i.symbols = interface
   dotnet_naming_rule.interfaces_should_be_prefixed_with_i.style = begins_with_i

   # StyleCop rules
   dotnet_diagnostic.SA1633.severity = none  # File header
   dotnet_diagnostic.SA1200.severity = none  # Using directives placement
   ```

3. **ASP.NET Core Web API**

   **Minimal API** [accessed 2025-10-26](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis)
   ```xml
   <Project Sdk="Microsoft.NET.Sdk.Web">
     <PropertyGroup>
       <TargetFramework>net8.0</TargetFramework>
       <Nullable>enable</Nullable>
       <ImplicitUsings>enable</ImplicitUsings>
     </PropertyGroup>

     <ItemGroup>
       <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="8.0.4" />
       <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
     </ItemGroup>
   </Project>
   ```

   Program.cs (minimal API):
   ```csharp
   var builder = WebApplication.CreateBuilder(args);

   builder.Services.AddEndpointsApiExplorer();
   builder.Services.AddSwaggerGen();

   var app = builder.Build();

   if (app.Environment.IsDevelopment())
   {
       app.UseSwagger();
       app.UseSwaggerUI();
   }

   app.UseHttpsRedirection();

   app.MapGet("/api/health", () => Results.Ok(new { status = "healthy" }))
      .WithName("GetHealth")
      .WithOpenApi();

   app.Run();
   ```

4. **Blazor WebAssembly**

   ```xml
   <Project Sdk="Microsoft.NET.Sdk.BlazorWebAssembly">
     <PropertyGroup>
       <TargetFramework>net8.0</TargetFramework>
     </PropertyGroup>

     <ItemGroup>
       <PackageReference Include="Microsoft.AspNetCore.Components.WebAssembly" Version="8.0.4" />
       <PackageReference Include="Microsoft.AspNetCore.Components.WebAssembly.DevServer" Version="8.0.4" PrivateAssets="all" />
     </ItemGroup>
   </Project>
   ```

---

### T3: Advanced Configuration (≤12k tokens)

**Deep configuration for NuGet packaging and production:**

1. **NuGet Package Configuration** [accessed 2025-10-26](https://learn.microsoft.com/en-us/nuget/create-packages/creating-a-package-msbuild)

   ```xml
   <Project Sdk="Microsoft.NET.Sdk">
     <PropertyGroup>
       <TargetFramework>net8.0</TargetFramework>
       <GeneratePackageOnBuild>true</GeneratePackageOnBuild>
       <PackageId>CompanyName.ProjectName</PackageId>
       <Version>1.0.0</Version>
       <Authors>Your Name</Authors>
       <Company>Company Name</Company>
       <Description>Package description</Description>
       <PackageTags>tag1;tag2;tag3</PackageTags>
       <PackageLicenseExpression>MIT</PackageLicenseExpression>
       <PackageProjectUrl>https://github.com/user/repo</PackageProjectUrl>
       <RepositoryUrl>https://github.com/user/repo</RepositoryUrl>
       <RepositoryType>git</RepositoryType>
       <PublishRepositoryUrl>true</PublishRepositoryUrl>
       <EmbedUntrackedSources>true</EmbedUntrackedSources>
       <IncludeSymbols>true</IncludeSymbols>
       <SymbolPackageFormat>snupkg</SymbolPackageFormat>
     </PropertyGroup>

     <ItemGroup>
       <PackageReference Include="Microsoft.SourceLink.GitHub" Version="8.0.0" PrivateAssets="All" />
     </ItemGroup>
   </Project>
   ```

2. **Multi-Target Framework**

   ```xml
   <PropertyGroup>
     <TargetFrameworks>net6.0;net7.0;net8.0</TargetFrameworks>
   </PropertyGroup>

   <ItemGroup Condition="'$(TargetFramework)' == 'net6.0'">
     <PackageReference Include="System.Text.Json" Version="6.0.0" />
   </ItemGroup>

   <ItemGroup Condition="'$(TargetFramework)' == 'net8.0'">
     <PackageReference Include="System.Text.Json" Version="8.0.0" />
   </ItemGroup>
   ```

3. **Native AOT Publishing** [accessed 2025-10-26](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/)

   ```xml
   <PropertyGroup>
     <PublishAot>true</PublishAot>
     <InvariantGlobalization>true</InvariantGlobalization>
     <JsonSerializerIsReflectionEnabledByDefault>false</JsonSerializerIsReflectionEnabledByDefault>
   </PropertyGroup>
   ```

   Publish command:
   ```bash
   dotnet publish -c Release -r linux-x64 --self-contained
   ```

4. **Docker Configuration**

   Dockerfile (multi-stage):
   ```dockerfile
   FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
   WORKDIR /src
   COPY ["src/ProjectName/ProjectName.csproj", "src/ProjectName/"]
   RUN dotnet restore "src/ProjectName/ProjectName.csproj"
   COPY . .
   WORKDIR "/src/src/ProjectName"
   RUN dotnet build "ProjectName.csproj" -c Release -o /app/build

   FROM build AS publish
   RUN dotnet publish "ProjectName.csproj" -c Release -o /app/publish

   FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
   WORKDIR /app
   EXPOSE 8080
   COPY --from=publish /app/publish .
   ENTRYPOINT ["dotnet", "ProjectName.dll"]
   ```

   .dockerignore:
   ```
   **/bin
   **/obj
   **/out
   **/.vs
   **/.vscode
   ```

5. **CI/CD Pipeline** (GitHub Actions)

   ```.github/workflows/dotnet.yml
   name: .NET CI

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
       - name: Setup .NET
         uses: actions/setup-dotnet@v4
         with:
           dotnet-version: 8.0.x
       - name: Restore dependencies
         run: dotnet restore
       - name: Build
         run: dotnet build --no-restore
       - name: Test
         run: dotnet test --no-build --verbosity normal --collect:"XPlat Code Coverage"
       - name: Upload coverage
         uses: codecov/codecov-action@v4
   ```

6. **Solution-Level Configuration**

   Directory.Build.props (applies to all projects):
   ```xml
   <Project>
     <PropertyGroup>
       <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
       <AnalysisMode>AllEnabledByDefault</AnalysisMode>
       <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
       <EnableNETAnalyzers>true</EnableNETAnalyzers>
     </PropertyGroup>
   </Project>
   ```

---

## Decision Rules

**Project Type Selection:**
- **library:** Class library for NuGet distribution, multi-targeting
- **console:** Command-line application, single executable
- **web-api:** ASP.NET Core minimal API or MVC for REST services
- **blazor:** Blazor WebAssembly or Server for SPAs
- **wpf:** Windows desktop application (Windows-only)
- **maui:** Cross-platform mobile and desktop (.NET MAUI)

**Test Framework Selection:**
- **xUnit:** Modern, recommended for new projects, parallel execution
- **NUnit:** Mature, feature-rich, parameterized tests
- **MSTest:** Microsoft's framework, Visual Studio integration

**Abort Conditions:**
- Invalid `project_name` (contains spaces, special chars) → error
- Conflicting frameworks (WPF + MAUI) → error
- Unsupported .NET version → error

**.NET Version Selection:**
- Use .NET 8.0 for new projects (LTS with long-term support)
- .NET 6.0 for compatibility with older systems (LTS)
- .NET 7.0 for latest features (standard support)

---

## Output Contract

**Schema (JSON):**

```json
{
  "project_name": "string",
  "project_type": "library | console | web-api | blazor | wpf | maui",
  "dotnet_version": "string",
  "test_framework": "xunit | nunit | mstest",
  "structure": {
    "directories": ["string"],
    "files": {
      "path/to/file": "file content (string)"
    }
  },
  "commands": {
    "restore": "string",
    "build": "string",
    "test": "string",
    "run": "string",
    "publish": "string"
  },
  "next_steps": ["string"],
  "timestamp": "ISO-8601 string (NOW_ET)"
}
```

**Required Fields:**
- All fields mandatory
- File contents must be syntactically valid (XML, C#, JSON)
- Include inline comments explaining configuration choices

---

## Examples

**Example 1: ASP.NET Core Web API with xUnit**

```
INPUT: {
  project_type: "web-api",
  dotnet_version: "8.0",
  test_framework: "xunit",
  project_name: "PaymentService"
}

OUTPUT:
structure:
  - src/PaymentService/
    - PaymentService.csproj
    - Program.cs
    - appsettings.json
  - tests/PaymentService.Tests/
    - PaymentService.Tests.csproj
    - HealthCheckTests.cs
  - PaymentService.sln

commands:
  restore: "dotnet restore"
  build: "dotnet build"
  test: "dotnet test"
  run: "dotnet run --project src/PaymentService"
  publish: "dotnet publish -c Release"
```

_(Full output truncated for ≤30 line limit)_

---

## Quality Gates

**Token Budgets:**
- **T1:** ≤2k tokens (basic structure + .csproj + .sln)
- **T2:** ≤6k tokens (testing, analyzers, ASP.NET Core, Blazor)
- **T3:** ≤12k tokens (NuGet packaging, multi-targeting, Docker, CI/CD, native AOT)

**Safety:**
- No hardcoded API keys or secrets
- .gitignore includes bin/, obj/, .vs/, .user files
- Roslyn analyzers configured to catch security issues

**Auditability:**
- All configurations cite official Microsoft documentation
- Version constraints explicit
- Generation timestamp included

**Determinism:**
- Same inputs → identical structure
- Versions pinned where appropriate
- No randomness in generation

**Performance:**
- T1 generation: <1 second
- T2 generation: <3 seconds
- T3 generation: <5 seconds

---

## Resources

**Official Documentation (accessed 2025-10-26):**
1. [.NET Documentation](https://learn.microsoft.com/en-us/dotnet/core/) - Core .NET reference
2. [ASP.NET Core Documentation](https://learn.microsoft.com/en-us/aspnet/core/) - Web framework
3. [xUnit Getting Started](https://xunit.net/docs/getting-started/netcore/) - Testing framework
4. [NuGet Documentation](https://learn.microsoft.com/en-us/nuget/) - Package management
5. [StyleCop Analyzers](https://github.com/DotNetAnalyzers/StyleCopAnalyzers) - Code quality
6. [Blazor Documentation](https://learn.microsoft.com/en-us/aspnet/core/blazor/) - WebAssembly/Server
7. [.NET MAUI Documentation](https://learn.microsoft.com/en-us/dotnet/maui/) - Cross-platform apps

**Testing:**
- [NUnit](https://docs.nunit.org/) - Alternative testing framework
- [MSTest](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-mstest) - Microsoft testing framework
- [Moq](https://github.com/moq/moq4) - Mocking library
- [FluentAssertions](https://fluentassertions.com/) - Assertion library

**Build Tools:**
- [MSBuild](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild) - Build engine
- [Native AOT](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/) - Ahead-of-time compilation

**Best Practices:**
- [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) - Style guide
- [.NET Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/) - API design
